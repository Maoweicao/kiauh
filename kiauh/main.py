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

from core.logger import Logger
from core.menus.main_menu import MainMenu
from core.settings.kiauh_settings import KiauhSettings


def ensure_encoding() -> None:
    if sys.stdout.encoding == "UTF-8" or not isinstance(sys.stdout, io.TextIOWrapper):
        return
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    import locale
    import os
    import subprocess
    first_run_flag = os.path.join(os.path.dirname(__file__), '.kiauh_first_run')
    if not os.path.exists(first_run_flag):
        # 检测系统语言
        lang, encoding = locale.getdefaultlocale()
        Logger.print_ok(f"当前系统语言: {lang or '未知'} (编码: {encoding or '未知'})", prefix=False)
        # 检查能否 ping 通谷歌
        try:
            # Windows 下 ping -n 1，Linux/macOS 下 ping -c 1
            ping_cmd = ['ping', 'www.google.com', '-n', '1'] if sys.platform.startswith('win') else ['ping', 'www.google.com', '-c', '1']
            result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                Logger.print_ok("网络检测: 可以访问谷歌 (www.google.com)", prefix=False)
            else:
                Logger.print_ok("网络检测: 无法访问谷歌 (www.google.com)", prefix=False)
        except Exception as e:
            Logger.print_ok(f"网络检测异常: {e}", prefix=False)
        # 创建标记文件
        with open(first_run_flag, 'w', encoding='utf-8') as f:
            f.write('shown')
    try:
        KiauhSettings()
        ensure_encoding()
        MainMenu().run()
    except KeyboardInterrupt:
        Logger.print_ok("\nHappy printing!\n", prefix=False)
