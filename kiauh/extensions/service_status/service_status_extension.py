# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #

import re
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List, Optional, Tuple

from core.logger import Logger
from extensions.base_extension import BaseExtension
from extensions.service_status import (
    FLUIDD_DIR,
    KLIPPER_SERVICE,
    MAINSAIL_DIR,
    MOONRAKER_SERVICE,
    NGINX_SERVICE,
    NGINX_SITES_ENABLED,
)
from utils.sys_utils import is_service_active


class ServiceStatusExtension(BaseExtension):
    def install_extension(self, **kwargs) -> None:
        Logger.print_info("This extension only checks service status.")
        Logger.print_info("No installation required.")
        self.show_status()

    def remove_extension(self, **kwargs) -> None:
        Logger.print_info("This extension only checks service status.")
        Logger.print_info("No removal required.")

    def show_status(self) -> None:
        Logger.print_header("Service Status")
        print()

        services = self._get_services_status()
        for service_name, status, detail in services:
            status_icon = "\033[32m●\033[0m" if status else "\033[31m●\033[0m"
            status_text = (
                "\033[32mRunning\033[0m" if status else "\033[31mStopped\033[0m"
            )
            detail_text = f" ({detail})" if detail else ""
            print(f"  {status_icon} {service_name:<20} {status_text}{detail_text}")

        print()
        self._show_summary(services)

    def _get_services_status(self) -> List[Tuple[str, bool, str]]:
        results: List[Tuple[str, bool, str]] = []

        results.append(("Klipper", is_service_active(KLIPPER_SERVICE), ""))
        results.append(("Moonraker", is_service_active(MOONRAKER_SERVICE), ""))

        nginx_active = is_service_active(NGINX_SERVICE)
        mainsail_port = self._get_nginx_port("mainsail")
        fluidd_port = self._get_nginx_port("fluidd")

        mainsail_installed = MAINSAIL_DIR.exists()
        fluidd_installed = FLUIDD_DIR.exists()

        if mainsail_installed and nginx_active and mainsail_port:
            port_ok = self._check_http_port(mainsail_port)
            detail = f"port {mainsail_port}"
            results.append(("Mainsail", port_ok, detail))
        else:
            results.append(
                ("Mainsail", False, "not installed" if not mainsail_installed else "")
            )

        if fluidd_installed and nginx_active and fluidd_port:
            port_ok = self._check_http_port(fluidd_port)
            detail = f"port {fluidd_port}"
            results.append(("Fluidd", port_ok, detail))
        else:
            results.append(
                ("Fluidd", False, "not installed" if not fluidd_installed else "")
            )

        return results

    def _get_nginx_port(self, client_name: str) -> Optional[int]:
        if not NGINX_SITES_ENABLED.exists():
            return None

        for config in NGINX_SITES_ENABLED.iterdir():
            if not config.is_file() or client_name not in config.name.lower():
                continue

            port = self._parse_listen_port(config)
            if port is not None:
                return port

        return None

    @staticmethod
    def _parse_listen_port(config: Path) -> Optional[int]:
        pattern = r"default_server|http://|https://|[;\[\]]"
        port = ""
        try:
            with open(config, "r") as cfg:
                for line in cfg.readlines():
                    line = re.sub(pattern, "", line.strip())
                    if line.startswith("listen"):
                        if ":" not in line:
                            port = line.split()[-1]
                        else:
                            port = line.split(":")[-1]
            return int(port)
        except (ValueError, OSError):
            return None

    @staticmethod
    def _check_http_port(port: int) -> bool:
        try:
            result = run(
                [
                    "curl",
                    "-s",
                    "-o",
                    "/dev/null",
                    "-w",
                    "%{http_code}",
                    "--connect-timeout",
                    "3",
                    f"http://127.0.0.1:{port}",
                ],
                capture_output=True,
                text=True,
                timeout=5,
            )
            return result.stdout.strip() in ("200", "304")
        except (CalledProcessError, FileNotFoundError, TimeoutError):
            return False

    def _show_summary(self, services: List[Tuple[str, bool, str]]) -> None:
        running_count = sum(1 for _, status, _ in services if status)
        total_count = len(services)

        if running_count == total_count:
            Logger.print_ok(f"All services are running ({running_count}/{total_count})")
        elif running_count == 0:
            Logger.print_warn(f"No services are running (0/{total_count})")
        else:
            Logger.print_warn(
                f"Some services are running ({running_count}/{total_count})"
            )
