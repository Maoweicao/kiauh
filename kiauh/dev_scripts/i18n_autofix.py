#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
自动化 i18n 修补工具（谨慎模式）
根据 `i18n_audit_report.md`（dev_scripts）中的硬编码字符串列表，
在代码中把文字常量替换为 `translate('<key>')` 调用。

默认运行为 dry-run，只会打印拟议修改；使用 --apply 才会写回文件，
并会在修改前保存备份 `<file>.bak`。

注意：替换限于 AST 中字面字符串常量（非拼接或复杂表达式）；
请在 CI/本地确认后再使用 --apply。
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
import ast
import hashlib


def create_key_from_text(text: str) -> str:
    import re
    clean_text = re.sub(r"[^\w\s]", "", text)
    words = clean_text.lower().split()
    if len(words) > 5:
        words = words[:5]
    key = '_'.join(words)
    if not key:
        key = f"text_{abs(hash(text)) % 10000}"
    # Ensure key length safe
    return key


def parse_audit_report(report_path: Path) -> Dict[Path, Set[str]]:
    """从 markdown 报告中解析出每个文件对应的硬编码字符串集合"""
    files: Dict[Path, Set[str]] = {}
    cur_file = None
    in_hard_section = False

    code_tick_re = re.compile(r"`([^`]+)`")
    file_header_re = re.compile(r"^###\s+(.*)$")

    for line in report_path.read_text(encoding='utf-8').splitlines():
        m = file_header_re.match(line)
        if m:
            raw = m.group(1).strip()
            # raw may be relative path like kiauh\components\... or similar
            # try to build path relative to repo root
            # We expect paths to start with 'kiauh' typically
            cur_file = Path(raw)
            in_hard_section = False
            continue

        # sections are indicated with **硬编码字符串示例**:
        if line.strip().startswith('**硬编码字符串示例**'):
            in_hard_section = True
            continue

        # next section or blank ends hard section
        if in_hard_section and line.strip().startswith('**') and not line.strip().startswith('**硬编码'):
            in_hard_section = False

        if in_hard_section and cur_file is not None:
            # try to find backtick quoted snippet
            m2 = code_tick_re.search(line)
            if m2:
                txt = m2.group(1)
                if txt:
                    # normalize path to repo style
                    # if cur_file is relative, keep as-is
                    files.setdefault(cur_file, set()).add(txt)
    return files


class ReplaceTranslator(ast.NodeTransformer):
    """AST 转换器：把匹配的字符串常量替换为 translate('key') 调用。
    会尽量避开已经在 translate() 内部的字符串。
    """
    def __init__(self, targets: Set[str], file_path: Path):
        super().__init__()
        self.targets = targets
        self.file_path = file_path
        self.replaced = 0
        self.seen_keys = {}
        self.parent_stack = []

    def generic_visit(self, node):
        self.parent_stack.append(node)
        res = super().generic_visit(node)
        self.parent_stack.pop()
        return res

    def in_translate_call(self):
        # check if any parent is a Call with func named translate
        for node in reversed(self.parent_stack):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'translate':
                return True
        return False

    def visit_Constant(self, node: ast.Constant):
        # only replace string constants
        if not isinstance(node.value, str):
            return node
        val = node.value
        if val in self.targets and not self.in_translate_call():
            # build a translate('key') call
            base_key = create_key_from_text(val)
            # make short hash to avoid collisions
            short_hash = hashlib.sha1(val.encode('utf-8')).hexdigest()[:6]
            key = f"{base_key}_{short_hash}"
            # ensure deterministic
            if key in self.seen_keys:
                key = self.seen_keys[key]
            else:
                self.seen_keys[key] = key

            new = ast.Call(func=ast.Name(id='translate', ctx=ast.Load()), args=[ast.Constant(value=key)], keywords=[])
            ast.copy_location(new, node)
            ast.fix_missing_locations(new)
            self.replaced += 1
            return new
        return node


def process_file(path: Path, targets: Set[str], apply_changes: bool, backup: bool) -> int:
    src = path.read_text(encoding='utf-8')
    try:
        tree = ast.parse(src)
    except Exception as e:
        print(f"  [skip] parse error: {path}: {e}")
        return 0

    replacer = ReplaceTranslator(targets, path)
    new_tree = replacer.visit(tree)
    if replacer.replaced == 0:
        return 0

    # need to unparse AST back to source
    try:
        new_src = ast.unparse(new_tree)
    except Exception:
        try:
            # try astor as fallback for older Python versions
            try:
                import astor  # type: ignore
                new_src = astor.to_source(new_tree)
            except Exception:
                print(f"  [error] cannot unparse AST for {path}. Python >=3.9 or astor package required.")
                return 0
        except Exception:
            print(f"  [error] cannot unparse AST for {path}. Python >=3.9 or astor package required.")
            return 0

    if apply_changes:
        if backup:
            bak = path.with_suffix(path.suffix + '.bak')
            bak.write_text(src, encoding='utf-8')
        path.write_text(new_src, encoding='utf-8')
        print(f"  [apply] {path} -> {replacer.replaced} replacements (backup: {backup})")
    else:
        print(f"  [dry-run] {path} -> {replacer.replaced} replacements")

    return replacer.replaced


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--report', default=None, help='审计报告路径（默认 dev_scripts/i18n_audit_report.md）')
    p.add_argument('--apply', action='store_true', help='执行写回修改（默认 dry-run）')
    p.add_argument('--no-backup', dest='backup', action='store_false', help='在 apply 时不创建备份')
    p.add_argument('--preview', type=int, default=10, help='dry-run 时每个文件显示前 N 个示例（默认 10）')
    args = p.parse_args()

    script_dir = Path(__file__).resolve().parent
    report_path = Path(args.report) if args.report else script_dir / 'i18n_audit_report.md'
    if not report_path.exists():
        print(f"ERROR: report not found: {report_path}")
        sys.exit(1)

    parsed = parse_audit_report(report_path)
    if not parsed:
        print('No hard-coded strings parsed from report.')
        return

    total_candidates = sum(len(s) for s in parsed.values())
    print(f'Parsed {len(parsed)} files, total {total_candidates} string candidates from report')

    summary = {}
    for raw_path, strings in parsed.items():
        # try to resolve path relative to repo root: path may be like kiauh\components\...
        if raw_path.is_absolute():
            real = raw_path
        else:
            # project root assumed two parents up from script
            project_root = script_dir.parents[1]
            real = project_root.joinpath(raw_path)
            # try with forward/back slashes normalized
            if not real.exists():
                alt = project_root.joinpath(str(raw_path).replace('\\', '/'))
                if alt.exists():
                    real = alt

        if not real.exists():
            print(f'  [warn] file not found: {raw_path} -> tried {real}')
            continue

        # find occurrences in file to ensure literal match
        src = real.read_text(encoding='utf-8')
        found = set()
        for s in strings:
            if s in src:
                found.add(s)
        if not found:
            print(f'  [skip] no literal occurrences in file: {real}')
            continue

        # For dry-run, list preview
        if not args.apply:
            print(f'File: {real} -> {len(found)} candidates')
            for i, s in enumerate(sorted(found)):
                if i >= args.preview:
                    print(f'  ... and {len(found)-args.preview} more')
                    break
                print(f'  - {s}')

        changed = process_file(real, found, args.apply, args.backup)
        summary[str(real)] = changed

    total_replacements = sum(summary.values())
    print('\nSummary:')
    for fp, c in summary.items():
        print(f'  {fp}: {c}')
    print(f'Total replacements performed: {total_replacements} (apply={args.apply})')


if __name__ == '__main__':
    main()
