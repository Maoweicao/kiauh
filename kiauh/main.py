# ======================================================================= #
#  Copyright (C) 2020 - 2025 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #
import io
import sys
import locale
import os
import json
import subprocess

from core.logger import Logger
from core.menus.main_menu import MainMenu
from core.settings.kiauh_settings import KiauhSettings
def load_locale():
    lang, encoding = locale.getdefaultlocale()
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

def translate(key, **kwargs):
    text = TRANSLATIONS.get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


def ensure_encoding() -> None:
    if sys.stdout.encoding == "UTF-8" or not isinstance(sys.stdout, io.TextIOWrapper):
        return
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    global TRANSLATIONS
    TRANSLATIONS, lang, encoding = load_locale()
    first_run_flag = os.path.join(os.path.dirname(__file__), '.kiauh_first_run')
    if not os.path.exists(first_run_flag):
        Logger.print_ok(translate('welcome'), prefix=False)
        Logger.print_ok(translate('system_language', lang=lang or '未知', encoding=encoding or '未知'), prefix=False)
        # 检查能否 ping 通谷歌
        try:
            ping_cmd = ['ping', 'www.google.com', '-n', '1'] if sys.platform.startswith('win') else ['ping', 'www.google.com', '-c', '1']
            result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                Logger.print_ok(translate('network_google_ok'), prefix=False)
            else:
                Logger.print_ok(translate('network_google_fail'), prefix=False)
        except Exception as e:
            Logger.print_ok(translate('network_google_error', error=str(e)), prefix=False)
        with open(first_run_flag, 'w', encoding='utf-8') as f:
            f.write('shown')
    try:
        KiauhSettings()
        ensure_encoding()
        MainMenu().run()
    except KeyboardInterrupt:
        Logger.print_ok("\n" + translate('happy_printing') + "\n", prefix=False)
