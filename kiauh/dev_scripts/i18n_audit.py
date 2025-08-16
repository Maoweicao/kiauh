#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KIAUH 国际化审计工具
扫描项目中Python文件，列出硬编码的用户可见字符串、使用了 translate()/TRANSLATIONS 的位置
并生成审计报告 `i18n_audit_report.md` 到本脚本目录（dev_scripts）。
"""

import ast
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
import sys


class I18nAudit:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.exclude_dirs = {
            '__pycache__', '.git', '.vscode', 'node_modules',
            'venv', '.env', 'env', 'tests', 'test', 'dev_scripts',
            '.conda', '.venv', '.pyenv', 'site-packages', 'dist-packages',
            'pip-wheel-metadata', 'build', 'dist'
        }

        # file -> lists
        self.hard_strings: Dict[Path, List[Tuple[int, str, str]]] = {}
        self.translate_calls: Dict[Path, List[Tuple[int, str]]] = {}
        self.translations_lookups: Dict[Path, List[Tuple[int, str]]] = {}

    def should_exclude_path(self, path: Path) -> bool:
        for part in path.parts:
            if part in self.exclude_dirs or (part.startswith('.') and part not in {'.', '.git'}):
                return True
        return False

    def is_translatable_string(self, s: str) -> bool:
        text = s.strip()
        if not text:
            return False
        if len(text) == 1:
            return False
        if text.isdigit():
            return False
        if any(x in text for x in ['/', '\\', '.', '__']):
            return False
        if text.startswith('{') and text.endswith('}'):
            return False
        if any(x in text for x in ['^', '$', '[', ']', '(', ')', '*', '+', '?']):
            return False
        technical_terms = [
            'utf-8', 'ascii', 'http', 'https', 'www', 'com', 'org',
            'github', 'json', 'yaml', 'cfg', 'conf', 'service',
            'systemd', 'sudo', 'apt', 'pip', 'python', 'bash'
        ]
        if any(term in text.lower() for term in technical_terms):
            return False
        if any('\u4e00' <= c <= '\u9fff' for c in text):
            return True
        if len(text) > 20 and text.replace(' ', '').isalpha():
            return True
        # common user-facing words
        user_friendly_indicators = [
            'error', 'success', 'failed', 'install', 'remove',
            'update', 'warning', 'info', 'please', 'unable',
            'found', 'not found', 'complete', 'finished'
        ]
        if any(ind in text.lower() for ind in user_friendly_indicators):
            return True
        return False

    def scan_file(self, file_path: Path):
        if self.should_exclude_path(file_path):
            return

        try:
            src = file_path.read_text(encoding='utf-8')
        except Exception:
            return

        try:
            tree = ast.parse(src, filename=str(file_path))
        except Exception:
            return

        # Visitor
        class Visitor(ast.NodeVisitor):
            def __init__(self, outer: 'I18nAudit'):
                self.outer = outer

            def visit_Call(self, node: ast.Call):
                # translate(...) 调用
                if isinstance(node.func, ast.Name) and node.func.id == 'translate':
                    if node.args:
                        arg = node.args[0]
                        if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                            self.outer.translate_calls.setdefault(file_path, []).append((node.lineno, arg.value))
                        else:
                            self.outer.translate_calls.setdefault(file_path, []).append((node.lineno, '<non-literal>'))

                # TRANSLATIONS[...] 或 TRANSLATIONS.get(...)
                if isinstance(node.func, ast.Attribute):
                    # e.g. TRANSLATIONS.get('key')
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'TRANSLATIONS':
                        if node.args:
                            a = node.args[0]
                            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                                self.outer.translations_lookups.setdefault(file_path, []).append((node.lineno, a.value))
                            else:
                                self.outer.translations_lookups.setdefault(file_path, []).append((node.lineno, '<non-literal>'))

                # 直接索引 TRANSLATIONS['key'] 会在 Subscript 中处理
                # Logger.print_* 或 print() 的字符串参数也可能在 Call 里
                if isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == 'Logger' and node.func.attr.startswith('print_'):
                        if node.args:
                            a = node.args[0]
                            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                                self.outer.hard_strings.setdefault(file_path, []).append((node.lineno, a.value, 'Logger.print'))
                elif isinstance(node.func, ast.Name) and node.func.id == 'print':
                    for a in node.args:
                        if isinstance(a, ast.Constant) and isinstance(a.value, str):
                            self.outer.hard_strings.setdefault(file_path, []).append((node.lineno, a.value, 'print'))

                self.generic_visit(node)

            def visit_Subscript(self, node: ast.Subscript):
                # TRANSLATIONS['key']
                try:
                    if isinstance(node.value, ast.Name) and node.value.id == 'TRANSLATIONS':
                        key_node = node.slice
                        if isinstance(key_node, ast.Constant) and isinstance(key_node.value, str):
                            self.outer.translations_lookups.setdefault(file_path, []).append((node.lineno, key_node.value))
                except Exception:
                    pass
                self.generic_visit(node)

            def visit_Constant(self, node: ast.Constant):
                if isinstance(node.value, str):
                    if self.outer.is_translatable_string(node.value):
                        # try to find context from parent nodes by lineno info (best-effort)
                        self.outer.hard_strings.setdefault(file_path, []).append((node.lineno, node.value, 'constant'))
                self.generic_visit(node)

        v = Visitor(self)
        v.visit(tree)

        # 补充：用正则再查找 f-strings 和简单 print(...) 中的字符串（行级）
        lines = src.splitlines()
        for i, line in enumerate(lines, 1):
            if re.search(r"f\"|f'", line):
                # 捕获简单的 fstring 文本片段
                for m in re.finditer(rf"f[\"']([^\{{\}}\n]+)[\"']", line):
                    txt = m.group(1).strip()
                    if txt and self.is_translatable_string(txt):
                        self.hard_strings.setdefault(file_path, []).append((i, txt, 'fstring'))

    def scan_project(self) -> None:
        p = Path(self.project_root)
        kiauh_dir = None
        if (p / 'kiauh').is_dir():
            kiauh_dir = (p / 'kiauh').resolve()
        else:
            cur = p.resolve()
            while True:
                if cur.name == 'kiauh':
                    kiauh_dir = cur
                    break
                if cur.parent == cur:
                    break
                cur = cur.parent
        if kiauh_dir is None:
            kiauh_dir = p.resolve()

        for py_file in kiauh_dir.rglob('*.py'):
            if not self.should_exclude_path(py_file):
                self.scan_file(py_file)

    def generate_report(self):
        script_dir = Path(__file__).resolve().parent
        out = script_dir / 'i18n_audit_report.md'
        with open(out, 'w', encoding='utf-8') as f:
            from datetime import datetime
            f.write('# KIAUH 国际化审计报告\n\n')
            f.write(f'生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')

            total_hard = sum(len(v) for v in self.hard_strings.values())
            total_translate = sum(len(v) for v in self.translate_calls.values())
            total_lookup = sum(len(v) for v in self.translations_lookups.values())

            f.write(f'总结:\n\n- 硬编码可能需要国际化的文本: {total_hard}\n')
            f.write(f'- translate() 调用次数: {total_translate}\n')
            f.write(f'- TRANSLATIONS 查找次数: {total_lookup}\n\n')

            f.write('## 按文件详情\n\n')

            files = sorted(set(list(self.hard_strings.keys()) + list(self.translate_calls.keys()) + list(self.translations_lookups.keys())))
            for file_path in files:
                f.write(f'### {file_path.relative_to(Path(__file__).resolve().parents[2]) if file_path.is_absolute() else file_path}\n\n')

                hs = self.hard_strings.get(file_path, [])
                if hs:
                    f.write('**硬编码字符串示例**:\n\n')
                    for lineno, text, ctx in hs[:50]:
                        snippet = text.replace('```', "'``")
                        f.write(f'- L{lineno} ({ctx}): `{snippet}`\n')
                    f.write('\n')

                tc = self.translate_calls.get(file_path, [])
                if tc:
                    f.write('**translate() 调用**:\n\n')
                    for lineno, key in tc[:50]:
                        f.write(f'- L{lineno}: `{key}`\n')
                    f.write('\n')

                tl = self.translations_lookups.get(file_path, [])
                if tl:
                    f.write('**TRANSLATIONS 查找**:\n\n')
                    for lineno, key in tl[:50]:
                        f.write(f'- L{lineno}: `{key}`\n')
                    f.write('\n')

        print(f'审计报告已生成: {out}')


def main():
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        # 默认使用仓库根目录（上两级）
        project_root = Path(__file__).resolve().parents[2]

    audit = I18nAudit(str(project_root))
    print('开始审计KIAUH项目（可能需要几秒）...')
    audit.scan_project()
    audit.generate_report()


if __name__ == '__main__':
    main()
