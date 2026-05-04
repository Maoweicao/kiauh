# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #
from __future__ import annotations

import textwrap
from typing import Type

from components.klipper.klipper_utils import get_klipper_status
from components.moonraker.utils.utils import get_moonraker_status
from core.i18n import _, get_available_languages, reload_i18n
from core.logger import DialogType, Logger
from core.menus import Option
from core.menus.base_menu import BaseMenu
from core.menus.repo_select_menu import RepoSelectMenu
from core.settings.kiauh_settings import KiauhSettings
from core.types.color import Color
from core.types.component_status import ComponentStatus
from utils.input_utils import get_selection_input


# noinspection PyUnusedLocal
# noinspection PyMethodMayBeStatic
class SettingsMenu(BaseMenu):
    def __init__(self, previous_menu: Type[BaseMenu] | None = None) -> None:
        super().__init__()
        self.title = _("settings_menu.title")
        self.title_color = Color.CYAN
        self.previous_menu: Type[BaseMenu] | None = previous_menu

        self.mainsail_unstable: bool | None = None
        self.fluidd_unstable: bool | None = None
        self.auto_backups_enabled: bool | None = None
        self.current_language: str = "en"

        na: str = _("common.not_available")
        self.kl_repo_url: str = Color.apply(na, Color.RED)
        self.kl_branch: str = Color.apply(na, Color.RED)
        self.mr_repo_url: str = Color.apply(na, Color.RED)
        self.mr_branch: str = Color.apply(na, Color.RED)

        self._load_settings()

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from core.menus.main_menu import MainMenu

        self.previous_menu = previous_menu if previous_menu is not None else MainMenu

    def set_options(self) -> None:
        self.options = {
            "1": Option(method=self.switch_klipper_repo),
            "2": Option(method=self.switch_moonraker_repo),
            "3": Option(method=self.toggle_mainsail_release),
            "4": Option(method=self.toggle_fluidd_release),
            "5": Option(method=self.toggle_backup_before_update),
            "6": Option(method=self.select_language),
        }

    def print_menu(self) -> None:
        checked = f"[{Color.apply('x', Color.GREEN)}]"
        unchecked = "[ ]"

        o1 = checked if self.mainsail_unstable else unchecked
        o2 = checked if self.fluidd_unstable else unchecked
        o3 = checked if self.auto_backups_enabled else unchecked

        lang_map = get_available_languages()
        lang_display = lang_map.get(self.current_language, self.current_language)
        lang_color = Color.apply(lang_display, Color.CYAN)

        menu = textwrap.dedent(
            f"""
            ╟───────────────────────────────────────────────────────╢
            ║ 1) {_("settings_menu.switch_klipper_repo"):<52} ║
            ║    ● Current repository:                              ║
            ║    └► Repo: {self.kl_repo_url:50} ║
            ║    └► Branch: {self.kl_branch:48} ║
            ╟───────────────────────────────────────────────────────╢
            ║ 2) {_("settings_menu.switch_moonraker_repo"):<52} ║
            ║    ● Current repository:                              ║
            ║    └► Repo: {self.mr_repo_url:50} ║
            ║    └► Branch: {self.mr_branch:48} ║
            ╟───────────────────────────────────────────────────────╢
            ║ {_("settings_menu.install_unstable"):<53} ║
            ║ 3) {o1} Mainsail                                       ║
            ║ 4) {o2} Fluidd                                         ║
            ╟───────────────────────────────────────────────────────╢
            ║ {_("settings_menu.auto_backup"):<53} ║
            ║ 5) {o3} {_("settings_menu.backup_before_update"):<47} ║
            ╟───────────────────────────────────────────────────────╢
            ║ {_("settings_menu.language"):<53} ║
            ║ 6)   Language: {lang_color:<48} ║
            ╟───────────────────────────────────────────────────────╢
            """
        )[1:]
        print(menu, end="")

    def _load_settings(self) -> None:
        self.settings = KiauhSettings()
        self.auto_backups_enabled = self.settings.kiauh.backup_before_update
        self.mainsail_unstable = self.settings.mainsail.unstable_releases
        self.fluidd_unstable = self.settings.fluidd.unstable_releases
        self.current_language = self.settings.kiauh.language or "en"

        klipper_status: ComponentStatus = get_klipper_status()
        moonraker_status: ComponentStatus = get_moonraker_status()

        def trim_repo_url(repo: str) -> str:
            return repo.replace(".git", "").replace("https://", "").replace("git@", "")

        if klipper_status.repo:
            url = trim_repo_url(klipper_status.repo_url)
            self.kl_repo_url = Color.apply(url, Color.CYAN)
            self.kl_branch = Color.apply(klipper_status.branch, Color.CYAN)
        if moonraker_status.repo:
            url = trim_repo_url(moonraker_status.repo_url)
            self.mr_repo_url = Color.apply(url, Color.CYAN)
            self.mr_branch = Color.apply(moonraker_status.branch, Color.CYAN)

    def _warn_no_repos(self, name: str) -> None:
        Logger.print_dialog(
            DialogType.WARNING,
            [_("repo_select_menu.no_repos_warn", name=name)],
            center_content=True,
        )

    def switch_klipper_repo(self, **kwargs) -> None:
        repos = self.settings.klipper.repositories
        RepoSelectMenu("klipper", repos=repos, previous_menu=self.__class__).run()

    def switch_moonraker_repo(self, **kwargs) -> None:
        repos = self.settings.moonraker.repositories
        RepoSelectMenu("moonraker", repos=repos, previous_menu=self.__class__).run()

    def toggle_mainsail_release(self, **kwargs) -> None:
        self.mainsail_unstable = not self.mainsail_unstable
        self.settings.mainsail.unstable_releases = self.mainsail_unstable
        self.settings.save()

    def toggle_fluidd_release(self, **kwargs) -> None:
        self.fluidd_unstable = not self.fluidd_unstable
        self.settings.fluidd.unstable_releases = self.fluidd_unstable
        self.settings.save()

    def toggle_backup_before_update(self, **kwargs) -> None:
        self.auto_backups_enabled = not self.auto_backups_enabled
        self.settings.kiauh.backup_before_update = self.auto_backups_enabled
        self.settings.save()

    def select_language(self, **kwargs) -> None:
        lang_map = get_available_languages()
        if not lang_map:
            Logger.print_info("No language files available.")
            return

        lang_codes = list(lang_map.keys())
        lang_lines = []
        for i, code in enumerate(lang_codes, start=1):
            marker = "*" if code == self.current_language else " "
            lang_lines.append(f" [{marker}] {i}) {lang_map[code]} ({code})")

        Logger.print_dialog(
            DialogType.CUSTOM,
            custom_title=_("settings_menu.select_language"),
            content=lang_lines,
            center_content=False,
        )

        options = {str(i + 1): code for i, code in enumerate(lang_codes)}
        choice = get_selection_input(
            _("common.perform_action"),
            options,
        )

        selected_lang = options.get(choice)
        if selected_lang is None:
            return

        self.current_language = selected_lang
        self.settings.kiauh.language = selected_lang
        self.settings.save()
        reload_i18n(selected_lang)
        Logger.print_ok(
            _("settings_menu.language_changed", name=lang_map[selected_lang])
        )
