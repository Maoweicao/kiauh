# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #

from pathlib import Path
from subprocess import PIPE, CalledProcessError, run

from core.i18n import _
from core.logger import DialogType, Logger
from utils.common import check_install_dependencies, get_current_date
from utils.fs_utils import check_file_exist
from utils.input_utils import get_confirm, get_string_input


def change_system_hostname() -> None:
    Logger.print_dialog(
        DialogType.CUSTOM,
        [
            _("component.hostname_desc"),
            "\n\n",
            "http://<hostname>.local",
            "\n\n",
            "Example: If you set your hostname to 'my-printer', you can access an "
            "installed webinterface by typing 'http://my-printer.local' in the "
            "browser.",
        ],
        custom_title=_("component.hostname_title"),
    )
    if not get_confirm(_("component.hostname_confirm"), default_choice=False):
        return

    Logger.print_dialog(
        DialogType.CUSTOM,
        [
            _("component.hostname_rules"),
            "The name must not contain the following:",
            "\n\n",
            "● Any special characters",
            "● No leading or trailing '-'",
        ],
    )
    hostname = get_string_input(
        _("component.hostname_enter"),
        regex=r"^[a-z0-9]+([a-z0-9-]*[a-z0-9])?$",
    )
    if not get_confirm(
        _("component.hostname_change_confirm", name=hostname), default_choice=False
    ):
        Logger.print_info(_("component.hostname_abort"))
        return

    try:
        Logger.print_status(_("component.hostname_changing"))

        Logger.print_status(_("component.hostname_checking_deps"))
        check_install_dependencies({"avahi-daemon"}, include_global=False)

        Logger.print_status(_("component.hostname_backup_hosts"))
        hosts_file = Path("/etc/hosts")
        if not check_file_exist(hosts_file, True):
            cmd = ["sudo", "touch", hosts_file.as_posix()]
            run(cmd, stderr=PIPE, check=True)
        else:
            date_time = get_current_date()
            name = f"hosts.{date_time.get('date')}-{date_time.get('time')}.bak"
            hosts_file_backup = Path(f"/etc/{name}")
            cmd = [
                "sudo",
                "cp",
                hosts_file.as_posix(),
                hosts_file_backup.as_posix(),
            ]
            run(cmd, stderr=PIPE, check=True)
        Logger.print_ok()

        Logger.print_status(_("component.hostname_setting", name=hostname))
        cmd = ["sudo", "hostnamectl", "set-hostname", hostname]
        run(cmd, stderr=PIPE, check=True)
        Logger.print_ok()

        Logger.print_status(_("component.hostname_writing"))
        stdin = f"127.0.0.1       {hostname}\n"
        cmd = ["sudo", "tee", "-a", hosts_file.as_posix()]
        run(cmd, input=stdin.encode(), stderr=PIPE, stdout=PIPE, check=True)
        Logger.print_ok()

        Logger.print_ok(_("component.hostname_success"))
        Logger.print_ok(_("component.hostname_reboot"))

    except CalledProcessError as e:
        Logger.print_error(_("component.hostname_error", error=str(e)))
        return
