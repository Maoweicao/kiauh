import re
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
REPORT = os.path.join(ROOT, 'i18n_scan_report.md')
LOCALES_DIR = os.path.join(ROOT, 'kiauh', 'locales')
EN_PATH = os.path.join(LOCALES_DIR, 'en_US.json')
ZH_PATH = os.path.join(LOCALES_DIR, 'zh_CN.json')
OUT_EN = os.path.join(LOCALES_DIR, 'en_US.generated.json')
OUT_ZH = os.path.join(LOCALES_DIR, 'zh_CN.generated.json')
OUT_STRINGS = os.path.join(LOCALES_DIR, 'strings_scan.generated.json')

pattern = re.compile(r"###\s*\d+\.\s*`([^`]+)`[\s\S]*?\*\*原文\*\*:\s*\n\s*```(.*?)```", re.MULTILINE)

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def main():
    text = open(REPORT, 'r', encoding='utf-8').read()
    matches = pattern.findall(text)
    print(f'Found {len(matches)} entries in report')

    en = load_json(EN_PATH)
    zh = load_json(ZH_PATH)

    added_en = 0
    added_zh = 0

    for key, orig in matches:
        value = orig.strip()
        # normalize newlines for JSON
        value = value.replace('\r\n', '\n')
        if key not in en:
            en[key] = value
            added_en += 1
        if key not in zh:
            # if zh exists for the English text (unlikely), leave; else placeholder
            zh[key] = '[TO_TRANSLATE] ' + value
            added_zh += 1

    # dump generated files
    os.makedirs(LOCALES_DIR, exist_ok=True)
    with open(OUT_EN, 'w', encoding='utf-8') as f:
        json.dump(en, f, indent=2, ensure_ascii=False)
    with open(OUT_ZH, 'w', encoding='utf-8') as f:
        json.dump(zh, f, indent=2, ensure_ascii=False)

    # also create a strings_scan listing
    strings_scan = {k: (en.get(k) or zh.get(k) or '') for k, _ in matches}
    with open(OUT_STRINGS, 'w', encoding='utf-8') as f:
        json.dump(strings_scan, f, indent=2, ensure_ascii=False)

    print(f'Wrote {OUT_EN} ({added_en} new keys)')
    print(f'Wrote {OUT_ZH} ({added_zh} new keys)')
    print(f'Wrote {OUT_STRINGS} ({len(strings_scan)} keys)')

if __name__ == '__main__':
    main()
