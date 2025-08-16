"""Generate locale JSON files from i18n_scan_report.md.

Place this file under `kiauh/dev_scripts` and configure the LANGUAGES
list below to control which locale JSON files are generated (examples:
['en-US','zh-CN','zh-TW','zh-HK']).

Behaviour:
- Parse `i18n_scan_report.md` for keys and original English strings.
- For each selected locale, try to load existing locale file (e.g. `en_US.json`),
  preserve existing translations and add missing keys.
- For non-English locales, newly added entries are prefixed with
  '[TO_TRANSLATE] '. Generated files are written as `<locale>.generated.json`.

This script is intentionally simple and safe to run repeatedly.
"""

import re
import json
import os
import argparse
from typing import Dict, List


# Robust root and report detection. Ensure REPORT and ROOT are always strings.
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
# Prefer report file located in the same dev_scripts directory as this script
REPORT_DEV = os.path.join(_THIS_DIR, 'i18n_scan_report.md')
ROOT = os.path.abspath(os.path.join(_THIS_DIR, '..', '..'))
REPORT = REPORT_DEV if os.path.exists(REPORT_DEV) else os.path.join(ROOT, 'i18n_scan_report.md')

# If we didn't find the report in dev_scripts, fall back to searching common parent locations
if not os.path.exists(REPORT):
    POSSIBLE_ROOTS = [
        os.path.abspath(os.path.join(_THIS_DIR, '..', '..')),  # kiauh/kiauh -> kiauh
        os.path.abspath(os.path.join(_THIS_DIR, '..')),       # kiauh/dev_scripts
        os.path.abspath(os.path.join(_THIS_DIR, '..', '..', '..')),
    ]
    for root in POSSIBLE_ROOTS:
        candidate = os.path.join(root, 'i18n_scan_report.md')
        if os.path.exists(candidate):
            REPORT = candidate
            ROOT = root
            break

LOCALES_DIR = os.path.join(ROOT, 'kiauh', 'locales')
STRINGS_OUT = os.path.join(LOCALES_DIR, 'strings_scan.generated.json')

# Edit this list to choose which locales to generate by default.
# Use codes like 'en-US', 'zh-CN', 'zh-TW', 'zh-HK'.
LANGUAGES: List[str] = ['en-US', 'zh-CN', 'zh-TW', 'zh-HK']


pattern = re.compile(r"###\s*\d+\.\s*`([^`]+)`[\s\S]*?\*\*原文\*\*:\s*\n\s*```(.*?)```", re.MULTILINE)


def locale_to_filename(code: str) -> str:
    """Convert locale code like 'en-US' to filename 'en_US.json'."""
    parts = code.split('-')
    if len(parts) == 1:
        return f"{parts[0]}.json"
    return f"{parts[0].lower()}_{parts[1].upper()}.json"


def load_json(path: str) -> Dict[str, str]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def write_json(path: str, data: Dict[str, str]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def parse_report(report_path: str) -> List[tuple]:
    text = open(report_path, 'r', encoding='utf-8').read()
    matches = pattern.findall(text)
    return [(k, v.strip().replace('\r\n', '\n')) for k, v in matches]


def generate_locales(langs: List[str], report_path: str, locales_dir: str):
    matches = parse_report(report_path)
    print(f'Found {len(matches)} entries in report')

    generated_map: Dict[str, Dict[str, str]] = {}

    # Load existing locale files if present
    for code in langs:
        filename = locale_to_filename(code)
        path = os.path.join(locales_dir, filename)
        generated_map[code] = load_json(path)

    added_counts = {code: 0 for code in langs}

    # Use the English text from the report as the source value
    for key, orig in matches:
        for code in langs:
            loc = generated_map[code]
            if key in loc:
                continue
            # For English locales, place the original string.
            if code.lower().startswith('en'):
                loc[key] = orig
            else:
                loc[key] = '[TO_TRANSLATE] ' + orig
            added_counts[code] += 1

    # Write generated files
    for code in langs:
        filename = locale_to_filename(code)
        out_name = filename.replace('.json', '.generated.json')
        out_path = os.path.join(locales_dir, out_name)
        write_json(out_path, generated_map[code])
        print(f'Wrote {out_path} ({added_counts[code]} new keys)')

    # Also write a strings listing for quick review
    strings_scan = {}
    for k, _ in matches:
        strings_scan[k] = next((generated_map[code].get(k) for code in langs if generated_map[code].get(k)), '')
    write_json(STRINGS_OUT, strings_scan)
    print(f'Wrote {STRINGS_OUT} ({len(strings_scan)} keys)')


def main():
    parser = argparse.ArgumentParser(description='Generate locale JSON files from i18n_scan_report.md')
    parser.add_argument('--languages', '-l', help='Comma separated list of locale codes to generate (overrides built-in list)')
    parser.add_argument('--report', '-r', help='Path to i18n_scan_report.md (overrides auto-detected path)')
    args = parser.parse_args()

    langs = LANGUAGES
    if args.languages:
        langs = [s.strip() for s in args.languages.split(',') if s.strip()]

    print('Locales to generate:', langs)
    report_path = REPORT
    if args.report:
        report_path = args.report

    if not os.path.exists(report_path):
        print(f'ERROR: report not found at {report_path}')
        return

    generate_locales(langs, report_path, LOCALES_DIR)


if __name__ == '__main__':
    main()
