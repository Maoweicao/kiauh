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

from .translation import TranslationManager

_i18n = TranslationManager()


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


def get_current_language() -> str:
    return _i18n.current_language


def get_available_languages() -> dict[str, str]:
    """Returns {lang_code: display_name} for all available translations."""
    return _i18n.available_languages
