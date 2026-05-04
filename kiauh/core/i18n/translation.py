# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= =
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

LOCALES_DIR = Path(__file__).resolve().parent / "locales"


class TranslationManager:
    def __init__(self) -> None:
        self.current_language: str = "en"
        self._translations: Dict[str, Any] = {}
        self._available_languages: Dict[str, str] = {}
        self._load_available_languages()

    def _load_available_languages(self) -> None:
        if not LOCALES_DIR.is_dir():
            return
        for f in sorted(LOCALES_DIR.glob("*.json")):
            lang_code = f.stem
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    data = json.load(fh)
                display_name = data.get("meta", {}).get("language", lang_code)
                self._available_languages[lang_code] = display_name
            except (json.JSONDecodeError, OSError):
                continue

    @property
    def available_languages(self) -> Dict[str, str]:
        return dict(self._available_languages)

    def load_language(self, lang: str) -> None:
        lang_code = lang.split(".")[0].split("_")[0] if "_" in lang else lang
        locale_file = LOCALES_DIR / f"{lang}.json"
        if not locale_file.exists():
            locale_file = LOCALES_DIR / f"{lang_code}.json"
        if not locale_file.exists():
            locale_file = LOCALES_DIR / "en.json"

        self.current_language = lang
        try:
            with open(locale_file, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            self._translations = data.get("strings", {})
        except (json.JSONDecodeError, OSError):
            self._translations = {}

    def translate(self, key: str, *args, **kwargs) -> str:
        value = self._translations.get(key, key)
        if args:
            try:
                value = value % args
            except TypeError:
                pass
        if kwargs:
            try:
                value = value.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return value
