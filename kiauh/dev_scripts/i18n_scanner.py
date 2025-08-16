#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
KIAUH 国际化扫描工具
扫描项目中所有Python文件，提取需要国际化的字符串
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Tuple
import sys

class I18nScanner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.strings_to_translate = {}
        self.existing_translations = {}
        self.load_existing_translations()
        
        # 需要排除的目录和文件
        self.exclude_dirs = {
            '__pycache__', '.git', '.vscode', 'node_modules', 
            'venv', '.env', 'env', 'tests', 'test',
            'dev_scripts',
            # 常见运行环境或包目录（隐藏或虚拟环境）
            '.conda', '.venv', '.pyenv', 'site-packages', 'dist-packages',
            'pip-wheel-metadata', 'build', 'dist'
        }
        
        # 需要排除的文件模式
        self.exclude_files = {
            '*.pyc', '*.pyo', '*.pyd', '__pycache__', 
            'test_*.py', '*_test.py'
        }
        
        # 用于识别需要国际化的字符串的模式
        self.translation_patterns = [
            # Logger.print_* 调用
            r'Logger\.print_(?:ok|error|info|warn|warning|status)\s*\(\s*["\']([^"\']+)["\']',
            # print() 调用中的字符串
            r'print\s*\(\s*["\']([^"\']+)["\']',
            # 对话框文本
            r'DialogType\.\w+,\s*\[\s*["\']([^"\']+)["\']',
            # 菜单文本
            r'menu\s*=.*?["\']([^"\']+)["\']',
            # 错误消息
            r'raise\s+\w*Error\s*\(\s*["\']([^"\']+)["\']',
            # f-string 中的固定文本部分
            r'f["\']([^{}"\']*?)["\']',
        ]
    
    def load_existing_translations(self):
        """加载现有的翻译文件"""
        locales_dir = self.project_root / 'kiauh' / 'locales'
        if locales_dir.exists():
            for lang_file in locales_dir.glob('*.json'):
                try:
                    with open(lang_file, 'r', encoding='utf-8') as f:
                        lang_code = lang_file.stem
                        self.existing_translations[lang_code] = json.load(f)
                except Exception as e:
                    print(f"Error loading {lang_file}: {e}")
    
    def should_exclude_path(self, path: Path) -> bool:
        """检查路径是否应该被排除"""
        # 检查目录
        for part in path.parts:
            # 以点开头的隐藏目录通常是运行环境或配置目录，排除常见的
            if part in self.exclude_dirs or (part.startswith('.') and part not in {'.', '.git'}):
                return True
        
        # 检查文件模式
        for pattern in self.exclude_files:
            if path.match(pattern):
                return True
        
        return False
    
    def extract_strings_from_ast(self, file_path: Path) -> List[Tuple[str, int]]:
        """使用AST解析Python文件，提取字符串"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content, filename=str(file_path))
            strings = []
            
            class StringVisitor(ast.NodeVisitor):
                def visit_Call(self, node):
                    # 检查Logger调用
                    if (isinstance(node.func, ast.Attribute) and 
                        isinstance(node.func.value, ast.Name) and
                        node.func.value.id == 'Logger' and
                        node.func.attr.startswith('print_')):
                        
                        if node.args and isinstance(node.args[0], ast.Constant):
                            if isinstance(node.args[0].value, str):
                                strings.append((node.args[0].value, node.lineno))
                    
                    # 检查print调用
                    elif (isinstance(node.func, ast.Name) and 
                          node.func.id == 'print'):
                        for arg in node.args:
                            if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                                strings.append((arg.value, arg.lineno))
                    
                    self.generic_visit(node)
                
                def visit_Constant(self, node):
                    # 提取所有字符串常量
                    if isinstance(node.value, str) and len(node.value.strip()) > 0:
                        # 过滤掉一些不需要翻译的字符串
                        if self.is_translatable_string(node.value):
                            strings.append((node.value, node.lineno))
                    self.generic_visit(node)
                
                def is_translatable_string(self, text: str) -> bool:
                    """判断字符串是否需要翻译"""
                    text = text.strip()
                    
                    # 排除空字符串
                    if not text:
                        return False
                    
                    # 排除单个字符
                    if len(text) == 1:
                        return False
                    
                    # 排除纯数字
                    if text.isdigit():
                        return False
                    
                    # 排除路径相关
                    if any(x in text for x in ['/', '\\', '.', '__']):
                        return False
                    
                    # 排除格式化占位符
                    if text.startswith('{') and text.endswith('}'):
                        return False
                    
                    # 排除正则表达式
                    if any(x in text for x in ['^', '$', '[', ']', '(', ')', '*', '+', '?']):
                        return False
                    
                    # 排除技术术语和配置项
                    technical_terms = [
                        'utf-8', 'ascii', 'http', 'https', 'www', 'com', 'org',
                        'github', 'json', 'yaml', 'cfg', 'conf', 'service',
                        'systemd', 'sudo', 'apt', 'pip', 'python', 'bash'
                    ]
                    if any(term in text.lower() for term in technical_terms):
                        return False
                    
                    # 包含用户友好的文本
                    user_friendly_indicators = [
                        'error', 'success', 'failed', 'install', 'remove',
                        'update', 'warning', 'info', 'please', 'unable',
                        'found', 'not found', 'complete', 'finished'
                    ]
                    if any(indicator in text.lower() for indicator in user_friendly_indicators):
                        return True
                    
                    # 包含中文字符的肯定需要处理
                    if any('\u4e00' <= char <= '\u9fff' for char in text):
                        return True
                    
                    # 长度超过20的英文文本可能需要翻译
                    if len(text) > 20 and text.replace(' ', '').isalpha():
                        return True
                    
                    return False
            
            visitor = StringVisitor()
            visitor.visit(tree)
            return strings
            
        except Exception as e:
            print(f"Error parsing {file_path}: {e}")
            return []
    
    def extract_strings_with_regex(self, file_path: Path) -> List[Tuple[str, int]]:
        """使用正则表达式提取字符串"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            strings = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                for pattern in self.translation_patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        text = match.group(1).strip()
                        if text and len(text) > 1:
                            strings.append((text, i))
            
            return strings
            
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
    
    def scan_file(self, file_path: Path) -> Dict[str, List[Tuple[int, str]]]:
        """扫描单个文件"""
        if self.should_exclude_path(file_path):
            return {}
        
        print(f"Scanning: {file_path}")
        
        # 使用AST和正则表达式两种方法
        ast_strings = self.extract_strings_from_ast(file_path)
        regex_strings = self.extract_strings_with_regex(file_path)
        
        # 合并并去重
        all_strings = {}
        for text, line_no in ast_strings + regex_strings:
            if text not in all_strings:
                all_strings[text] = []
            all_strings[text].append((line_no, str(file_path)))
        
        return all_strings
    
    def scan_project(self) -> Dict[str, List[Tuple[int, str]]]:
        """扫描整个项目"""
        all_strings = {}
        # 尽量定位到仓库内的 kiauh 包目录进行扫描，避免扫描到脚本自身所在的 dev_scripts
        p = Path(self.project_root)
        kiauh_dir = None

        # 如果传入的路径旁有 'kiauh' 子目录，优先使用它
        if (p / 'kiauh').is_dir():
            kiauh_dir = (p / 'kiauh').resolve()
        else:
            # 向上查找最近的名为 kiauh 的父目录
            cur = p.resolve()
            while True:
                if cur.name == 'kiauh':
                    kiauh_dir = cur
                    break
                if cur.parent == cur:
                    break
                cur = cur.parent

        # 如果未找到 kiauh 目录，就使用传入的 project_root
        if kiauh_dir is None:
            kiauh_dir = p.resolve()

        # 扫描 kiauh_dir 下的 Python 文件
        for py_file in kiauh_dir.rglob('*.py'):
            if not self.should_exclude_path(py_file):
                file_strings = self.scan_file(py_file)
                for text, locations in file_strings.items():
                    if text not in all_strings:
                        all_strings[text] = []
                    all_strings[text].extend(locations)
        
        return all_strings
    
    def generate_translation_keys(self, strings: Dict[str, List[Tuple[int, str]]]) -> Dict[str, str]:
        """为字符串生成翻译键"""
        keys: Dict[str, str] = {}
        used_keys: Dict[str, int] = {}

        for text in strings.keys():
            base_key = self.create_key_from_text(text)
            count = used_keys.get(base_key, 0) + 1
            used_keys[base_key] = count

            key = base_key if count == 1 else f"{base_key}_{count}"
            keys[key] = text

        return keys
    
    def create_key_from_text(self, text: str) -> str:
        """从文本创建键名"""
        # 移除特殊字符，保留字母数字和空格
        clean_text = re.sub(r'[^\w\s]', '', text)

        # 转换为小写并用下划线连接
        words = clean_text.lower().split()

        # 限制键名长度
        if len(words) > 5:
            words = words[:5]

        key = '_'.join(words)

        # 确保键名不为空
        if not key:
            key = f"text_{hash(text) % 10000}"

        return key
    
    def update_translation_files(self, new_strings: Dict[str, str]):
        """更新翻译文件"""
        locales_dir = self.project_root / 'kiauh' / 'locales'
        
        for lang_code, translations in self.existing_translations.items():
            # 添加新的翻译键
            updated = False
            for key, english_text in new_strings.items():
                if key not in translations:
                    if lang_code == 'en_US':
                        translations[key] = english_text
                    else:
                        # 对于非英语语言，暂时使用英文作为占位符
                        translations[key] = f"[TO_TRANSLATE] {english_text}"
                    updated = True
            
            if updated:
                lang_file = locales_dir / f'{lang_code}.json'
                with open(lang_file, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, ensure_ascii=False, indent=2)
                print(f"Updated {lang_file}")
    
    def generate_report(self, strings: Dict[str, List[Tuple[int, str]]], keys: Dict[str, str]):
        """生成扫描报告"""
        # 始终把报告写入脚本所在的 dev_scripts 目录，确保输出位置固定
        script_dir = Path(__file__).resolve().parent
        report_file = script_dir / 'i18n_scan_report.md'
        from datetime import datetime

        def md_escape(text: str) -> str:
            # 简单的 Markdown 转义，避免破坏文档结构
            return text.replace('`', "'")

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("# KIAUH 国际化扫描报告\n\n")
            f.write(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总共发现 {len(strings)} 个需要翻译的字符串\n\n")

            f.write("## 字符串列表\n\n")

            # 为了保证输出稳定性，按键名排序
            for i, (key, text) in enumerate(sorted(keys.items(), key=lambda x: x[0]), 1):
                f.write(f"### {i}. `{md_escape(key)}`\n")
                f.write("**原文**:\n\n")
                # 对原文用代码块保护，避免特殊字符影响 markdown
                f.write("```")
                f.write(md_escape(text))
                f.write("```\n\n")

                locations = strings.get(text, [])
                f.write("**位置**:\n")
                if locations:
                    for line_no, file_path in locations[:5]:  # 只显示前5个位置
                        f.write(f"- {file_path}:{line_no}\n")

                    if len(locations) > 5:
                        f.write(f"- ...还有 {len(locations) - 5} 个位置\n")
                else:
                    f.write("- 无定位信息\n")

                f.write("\n")

        print(f"报告已生成: {report_file}")
    
    def run(self):
        """运行扫描"""
        print("开始扫描KIAUH项目...")
        
        # 扫描项目
        strings = self.scan_project()
        
        print(f"发现 {len(strings)} 个字符串需要处理")
        
        # 生成翻译键
        keys = self.generate_translation_keys(strings)
        
        # 生成报告
        self.generate_report(strings, keys)
        
        # 更新翻译文件
        self.update_translation_files(keys)
        
        print("扫描完成！")

def main():
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    else:
        project_root = os.path.dirname(__file__)
    
    scanner = I18nScanner(project_root)
    scanner.run()

if __name__ == '__main__':
    main()
