# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #
from __future__ import annotations

import locale
import re
import unicodedata

from .translation import TranslationManager

_i18n = TranslationManager()

_ANSI_RE = re.compile(r"\033\[[0-9;]*m")


def _(key: str, *args, **kwargs) -> str:
    return _i18n.translate(key, *args, **kwargs)


def init_i18n(settings_lang: str | None = None) -> str:
    import os

    lang = os.environ.get("KIAUH_LANG")
    if not lang:
        try:
            lang, _ = locale.getdefaultlocale()
        except ValueError:
            pass
    if not lang and settings_lang:
        lang = settings_lang
    if not lang:
        lang = "en"

    _i18n.load_language(lang)
    return _i18n.current_language


def reload_i18n(lang: str) -> str:
    """Reload translations immediately (for in-session language switch)."""
    _i18n.load_language(lang)
    return _i18n.current_language


def get_current_language() -> str:
    return _i18n.current_language


def get_available_languages() -> dict[str, str]:
    """Returns {lang_code: display_name} for all available translations."""
    return _i18n.available_languages


def display_width(text: str) -> int:
    """Return terminal display width, skipping ANSI codes, handling CJK."""
    clean = _ANSI_RE.sub("", str(text))
    width = 0
    for ch in clean:
        ea = unicodedata.east_asian_width(ch)
        if ea in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def wc_ljust(text: str, width: int) -> str:
    """Left-justify within display width, CJK-aware."""
    dw = display_width(text)
    if dw >= width:
        return text
    return text + " " * (width - dw)


def wc_center(text: str, width: int, fillchar: str = " ") -> str:
    """Center within display width, CJK-aware."""
    dw = display_width(text)
    if dw >= width:
        return text
    left = (width - dw) // 2
    right = width - dw - left
    return fillchar * left + text + fillchar * right
