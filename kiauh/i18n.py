from __future__ import annotations
import json
import locale
import os
from typing import Dict, Tuple

TRANSLATIONS: Dict[str, str] = {}


def load_locale(lang: str | None = None) -> Tuple[Dict[str, str], str, str | None]:
    """Load translations for the given locale code.
    If lang is None, use the system default.
    Returns (translations, lang, encoding)
    """
    if not lang:
        lang, encoding = locale.getdefaultlocale()
    else:
        encoding = None
    if not lang:
        lang = 'en_US'
    locale_path = os.path.join(os.path.dirname(__file__), 'locales', f'{lang}.json')
    if not os.path.exists(locale_path):
        locale_path = os.path.join(os.path.dirname(__file__), 'locales', 'en_US.json')
    try:
        with open(locale_path, 'r', encoding='utf-8') as f:
            translations = json.load(f)
    except Exception:
        translations = {}
    return translations, lang, encoding


def set_locale(lang: str) -> None:
    """Set global TRANSLATIONS to a new language."""
    global TRANSLATIONS
    TRANSLATIONS, _, _ = load_locale(lang)


def translate(key: str, **kwargs) -> str:
    text = TRANSLATIONS.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text


# Initialize default translations on import
try:
    TRANSLATIONS, _, _ = load_locale()
except Exception:
    TRANSLATIONS = {}
