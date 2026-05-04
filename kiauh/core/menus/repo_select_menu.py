# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #
from __future__ import annotations

from typing import List, Literal, Type

from core.i18n import _
from core.logger import DialogType, Logger
from core.menus import Option
from core.menus.base_menu import BaseMenu
from core.settings.kiauh_settings import KiauhSettings, Repository
from core.types.color import Color
from procedures.switch_repo import run_switch_repo_routine
from utils.input_utils import get_confirm, get_number_input, get_string_input


# noinspection PyUnusedLocal
# noinspection PyMethodMayBeStatic
class RepoSelectMenu(BaseMenu):
    def __init__(
        self,
        name: Literal["klipper", "moonraker"],
        repos: List[Repository],
        previous_menu: Type[BaseMenu] | None = None,
    ) -> None:
        super().__init__()
        self.title_color = Color.CYAN
        self.previous_menu = previous_menu
        self.settings = KiauhSettings()
        self.input_label_txt = _("repo_select_menu.select_repository")
        self.name = name
        self.repos = repos

        if self.name == "klipper":
            self.title = _("repo_select_menu.klipper_title")

        elif self.name == "moonraker":
            self.title = _("repo_select_menu.moonraker_title")

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from core.menus.settings_menu import SettingsMenu

        self.previous_menu = (
            previous_menu if previous_menu is not None else SettingsMenu
        )

    def set_options(self) -> None:
        self.options = {}
        if self.repos:
            for idx, repo in enumerate(self.repos, start=1):
                self.options[str(idx)] = Option(
                    method=self.select_repository, opt_data=repo
                )
        self.options["a"] = Option(method=self.add_repository)
        self.options["r"] = Option(method=self.remove_repository)
        self.options["b"] = Option(method=self.go_back)

    def print_menu(self) -> None:
        menu = "╟───────────────────────────────────────────────────────╢\n"
        menu += f"║ {_('repo_select_menu.available_repos'):<52} ║\n"
        menu += "╟───────────────────────────────────────────────────────╢\n"
        for idx, repo in enumerate(self.repos, start=1):
            url = f"● Repo: {repo.url.replace('.git', '')}"
            branch = f"└► Branch: {repo.branch}"
            menu += f"║ {idx}) {Color.apply(url, Color.CYAN):<59} ║\n"
            menu += f"║    {Color.apply(branch, Color.CYAN):<59} ║\n"
        menu += "╟───────────────────────────────────────────────────────╢\n"
        menu += f"║ {_('repo_select_menu.add_repository'):<52} ║\n"
        menu += f"║ {_('repo_select_menu.remove_repository'):<52} ║\n"
        menu += "╟───────────────────────────────────────────────────────╢\n"
        print(menu, end="")

    def select_repository(self, **kwargs) -> None:
        repo: Repository = kwargs.get("opt_data")
        Logger.print_status(
            _("repo_select_menu.switching", name=self.name.capitalize())
        )
        run_switch_repo_routine(self.name, repo.url, repo.branch)

    def add_repository(self, **kwargs) -> None:
        while True:
            Logger.print_dialog(
                DialogType.CUSTOM,
                custom_title=_("repo_select_menu.enter_url"),
                content=[
                    _("repo_select_menu.url_note"),
                ],
            )
            url = get_string_input(
                _("repo_select_menu.repo_url"), allow_special_chars=True
            ).strip()

            Logger.print_dialog(
                DialogType.CUSTOM,
                custom_title=_("repo_select_menu.enter_branch"),
                content=[_("repo_select_menu.press_enter_default")],
                center_content=False,
            )
            branch = get_string_input(
                _("common.branch"), allow_special_chars=True, default="master"
            ).strip()
            Logger.print_dialog(
                DialogType.CUSTOM,
                custom_title=_("repo_select_menu.summary"),
                content=[
                    f"● {_('repo_select_menu.repo_url')}:    {url}",
                    f"● {_('common.branch')}: {branch}",
                ],
            )
            confirm = get_confirm(_("repo_select_menu.save_repo"))
            if confirm:
                repo = Repository(url, branch)
                if self.name == "klipper":
                    self.settings.klipper.repositories.append(repo)
                    self.settings.save()
                    self.repos = self.settings.klipper.repositories
                else:
                    self.settings.moonraker.repositories.append(repo)
                    self.settings.save()
                    self.repos = self.settings.moonraker.repositories
                Logger.print_ok(_("repo_select_menu.repo_added_saved"))

                # Refresh menu to show new repo immediately and update options
                self.set_options()
                self.run()
                break
            else:
                Logger.print_info(_("repo_select_menu.operation_cancelled"))
                break

    def remove_repository(self, **kwargs) -> None:
        repos = self.repos
        if not repos:
            Logger.print_info(_("repo_select_menu.no_repos"))
            return
        repo_lines = [
            f"{idx}) {repo.url} [{repo.branch}]"
            for idx, repo in enumerate(repos, start=1)
        ]
        Logger.print_dialog(
            DialogType.CUSTOM,
            custom_title=_("repo_select_menu.available_repos"),
            content=[*repo_lines],
        )
        idx = get_number_input(_("repo_select_menu.select_remove"), 1, len(repos))
        removed = repos.pop(idx - 1)
        if self.name == "klipper":
            self.settings.klipper.repositories = repos
            self.settings.save()
            self.repos = self.settings.klipper.repositories
        else:
            self.settings.moonraker.repositories = repos
            self.settings.save()
            self.repos = self.settings.moonraker.repositories
        Logger.print_ok(
            _("repo_select_menu.repo_removed", url=removed.url, branch=removed.branch)
        )

        # Refresh menu to show updated repo list and options
        self.set_options()
        self.run()

    def go_back(self, **kwargs) -> None:
        from core.menus.settings_menu import SettingsMenu

        SettingsMenu().run()
