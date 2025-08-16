from __future__ import annotations
import textwrap
import os
from typing import Type
from components.klipper.klipper_utils import get_klipper_status
from components.moonraker.utils.utils import get_moonraker_status
from core.logger import DialogType, Logger
from core.menus import Option
from core.menus.base_menu import BaseMenu
from core.menus.repo_select_menu import RepoSelectMenu
from core.settings.kiauh_settings import KiauhSettings
from core.types.color import Color
from core.types.component_status import ComponentStatus

class SettingsMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None) -> None:
        super().__init__()
        self.title = 'Settings Menu'
        self.title_color = Color.CYAN
        self.previous_menu: Type[BaseMenu] | None = previous_menu
        self.mainsail_unstable: bool | None = None
        self.fluidd_unstable: bool | None = None
        self.auto_backups_enabled: bool | None = None
        self.language: str | None = None
        na: str = 'Not available!'
        self.kl_repo_url: str = Color.apply(na, Color.RED)
        self.kl_branch: str = Color.apply(na, Color.RED)
        self.mr_repo_url: str = Color.apply(na, Color.RED)
        self.mr_branch: str = Color.apply(na, Color.RED)
        self._load_settings()

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from core.menus.main_menu import MainMenu
        self.previous_menu = previous_menu if previous_menu is not None else MainMenu

    def set_options(self) -> None:
        self.options = {'1': Option(method=self.switch_klipper_repo), '2': Option(method=self.switch_moonraker_repo), '3': Option(method=self.toggle_mainsail_release), '4': Option(method=self.toggle_fluidd_release), '5': Option(method=self.toggle_backup_before_update), '6': Option(method=self.change_language)}

    def print_menu(self) -> None:
        checked = f"[{Color.apply('x', Color.GREEN)}]"
        unchecked = '[ ]'
        o1 = checked if self.mainsail_unstable else unchecked
        o2 = checked if self.fluidd_unstable else unchecked
        o3 = checked if self.auto_backups_enabled else unchecked
        lang_display = self.language or 'en_US'
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ 1) Switch Klipper source repository                   ║\n            ║    ● Current repository:                              ║\n            ║    └► Repo: {self.kl_repo_url:50} ║\n            ║    └► Branch: {self.kl_branch:48} ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ 2) Switch Moonraker source repository                 ║\n            ║    ● Current repository:                              ║\n            ║    └► Repo: {self.mr_repo_url:50} ║\n            ║    └► Branch: {self.mr_branch:48} ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ Install unstable releases:                            ║\n            ║ 3) {o1} Mainsail                                       ║\n            ║ 4) {o2} Fluidd                                         ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ Auto-Backup:                                          ║\n            ║ 5) {o3} Backup before update                           ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ Language:                                             ║\n            ║ 6) {lang_display:50} ║\n            ╟───────────────────────────────────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def _load_settings(self) -> None:
        self.settings = KiauhSettings()
        self.auto_backups_enabled = self.settings.kiauh.backup_before_update
        self.language = self.settings.kiauh.language
        self.mainsail_unstable = self.settings.mainsail.unstable_releases
        self.fluidd_unstable = self.settings.fluidd.unstable_releases
        klipper_status: ComponentStatus = get_klipper_status()
        moonraker_status: ComponentStatus = get_moonraker_status()

        def trim_repo_url(repo: str) -> str:
            return repo.replace('.git', '').replace('https://', '').replace('git@', '')
        if not klipper_status.repo == '-':
            url = trim_repo_url(klipper_status.repo_url)
            self.kl_repo_url = Color.apply(url, Color.CYAN)
            self.kl_branch = Color.apply(klipper_status.branch, Color.CYAN)
        if not moonraker_status.repo == '-':
            url = trim_repo_url(moonraker_status.repo_url)
            self.mr_repo_url = Color.apply(url, Color.CYAN)
            self.mr_branch = Color.apply(moonraker_status.branch, Color.CYAN)

    def _warn_no_repos(self, name: str) -> None:
        Logger.print_dialog(DialogType.WARNING, [f'No {name} repositories configured in kiauh.cfg!'], center_content=True)

    def switch_klipper_repo(self, **kwargs) -> None:
        name = 'Klipper'
        repos = self.settings.klipper.repositories
        if not repos:
            self._warn_no_repos(name)
            return
        RepoSelectMenu(name.lower(), repos=repos, previous_menu=self.__class__).run()

    def switch_moonraker_repo(self, **kwargs) -> None:
        name = 'Moonraker'
        repos = self.settings.moonraker.repositories
        if not repos:
            self._warn_no_repos(name)
            return
        RepoSelectMenu(name.lower(), repos=repos, previous_menu=self.__class__).run()

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

    def change_language(self, **kwargs) -> None:
        locales_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
        locales_dir = os.path.abspath(locales_dir)
        choices = []
        try:
            for name in os.listdir(locales_dir):
                if name.endswith('.json'):
                    choices.append(name.replace('.json', '').replace('_', '-'))
        except Exception:
            choices = ['en-US']
        Logger.print_dialog(DialogType.ATTENTION, ['Select language:'])
        for i, c in enumerate(choices, 1):
            print(f'{i}) {c}')
        try:
            sel = input('Choose: ').strip()
            idx = int(sel) - 1
            if 0 <= idx < len(choices):
                chosen = choices[idx].replace('-', '_')
                self.settings.kiauh.language = chosen
                self.settings.save()
                self.language = chosen
                Logger.print_ok(f'Language set to {chosen}')
            else:
                Logger.print_ok(translate('invalid_selection_b9ae31'))
        except Exception:
            Logger.print_ok(translate('invalid_input_eb4b7e'))