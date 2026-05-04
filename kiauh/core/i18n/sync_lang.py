#!/usr/bin/env python3
# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #
"""
KIAUH i18n Sync Tool

Usage:
  # Sync all existing language JSONs against en.json (adds missing keys):
  python kiauh/core/i18n/sync_lang.py

  # Sync a specific language:
  python kiauh/core/i18n/sync_lang.py zh_CN

  # Generate a new language JSON from en.json template:
  python kiauh/core/i18n/sync_lang.py --new fr

  # Dry-run (show what would change without writing):
  python kiauh/core/i18n/sync_lang.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent / "locales"
BASE_LANG = "en"


def load_json(path: Path) -> dict | None:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error loading {path.name}: {e}", file=sys.stderr)
        return None


def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=4)
        fh.write("\n")


def deep_get(d: dict, *keys) -> dict:
    """Navigate into nested dict."""
    for k in keys:
        d = d.get(k, {})
    return d


def sync_language(
    base_data: dict, lang_data: dict | None, lang_code: str, dry_run: bool = False
) -> dict:
    """Sync a language JSON with the base (en.json)."""
    base_strings: dict = base_data.get("strings", {})
    lang_strings: dict = lang_data.get("strings", {}) if lang_data else {}

    added = 0
    filled = 0
    for key in base_strings:
        if key not in lang_strings:
            lang_strings[key] = base_strings[key]
            added += 1
        elif not lang_strings[key]:
            lang_strings[key] = base_strings[key]
            filled += 1

    if lang_data is None:
        lang_display = ""
        lang_data = {
            "meta": {
                "language": lang_display,
                "author": "KIAUH Community",
                "locale": lang_code,
            },
            "strings": lang_strings,
        }
    else:
        lang_data["strings"] = lang_strings
        if "locale" not in lang_data.get("meta", {}):
            lang_data.setdefault("meta", {})["locale"] = lang_code

    if not dry_run:
        target_path = LOCALES_DIR / f"{lang_code}.json"
        save_json(target_path, lang_data)
        if added > 0 or filled > 0:
            print(
                f"  [{lang_code}] Added {added}, filled {filled} empty."
                f" Please fill in translations in {target_path.name}"
            )
        else:
            print(f"  [{lang_code}] Already up to date.")
    else:
        if added > 0:
            print(f"  [{lang_code}] Would add {added} missing key(s).")
        else:
            print(f"  [{lang_code}] Already up to date.")

    return lang_data


def generate_new_lang(
    base_data: dict, lang_code: str, lang_name: str = "", dry_run: bool = False
) -> dict:
    """Generate a new language JSON from en.json template."""
    base_strings: dict = base_data.get("strings", {})

    lang_data = {
        "meta": {
            "language": lang_name or lang_code,
            "author": "KIAUH Community",
            "locale": lang_code,
        },
        "strings": {k: base_strings[k] for k in base_strings},
    }

    if not dry_run:
        target_path = LOCALES_DIR / f"{lang_code}.json"
        save_json(target_path, lang_data)
        print(
            f"  [{lang_code}] Created new language template with"
            f" {len(base_strings)} strings."
            f" Please fill in translations in {target_path.name}"
        )
    else:
        print(
            f"  [{lang_code}] Would create new template with"
            f" {len(base_strings)} strings."
        )

    return lang_data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync KIAUH i18n language files against en.json"
    )
    parser.add_argument(
        "lang",
        nargs="?",
        help="Sync specific language code (e.g. zh_CN, de, ja) or use --new",
    )
    parser.add_argument(
        "--new",
        dest="new_lang",
        metavar="CODE",
        help="Generate a new language JSON from en.json template",
    )
    parser.add_argument(
        "--name",
        help="Display name for new language (used with --new)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    args = parser.parse_args()

    base_path = LOCALES_DIR / f"{BASE_LANG}.json"
    if not base_path.exists():
        print(f"Error: Base language file not found: {base_path}", file=sys.stderr)
        sys.exit(1)

    base_data = load_json(base_path)
    if base_data is None:
        sys.exit(1)

    print(f"Base: {BASE_LANG}.json ({len(base_data.get('strings', {}))} strings)\n")

    if args.new_lang:
        generate_new_lang(
            base_data, args.new_lang, args.name or "", dry_run=args.dry_run
        )
        return

    if args.lang:
        # Sync a specific language
        lang_path = LOCALES_DIR / f"{args.lang}.json"
        lang_data = load_json(lang_path) if lang_path.exists() else None
        if lang_data is None and not lang_path.exists():
            print(f"  [{args.lang}] File not found — generating new template.")
            generate_new_lang(
                base_data, args.lang, args.name or "", dry_run=args.dry_run
            )
        else:
            sync_language(base_data, lang_data, args.lang, dry_run=args.dry_run)
    else:
        # Sync all existing language files
        for lang_file in sorted(LOCALES_DIR.glob("*.json")):
            if lang_file.stem == BASE_LANG:
                continue
            lang_data = load_json(lang_file)
            if lang_data is None:
                continue
            sync_language(base_data, lang_data, lang_file.stem, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
