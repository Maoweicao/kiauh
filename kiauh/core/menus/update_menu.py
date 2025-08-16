from __future__ import annotations
import textwrap
from typing import Callable, List, Type
from components.crowsnest.crowsnest import get_crowsnest_status, update_crowsnest
from components.klipper.klipper_utils import get_klipper_status
from components.klipper.services.klipper_setup_service import KlipperSetupService
from components.klipperscreen.klipperscreen import get_klipperscreen_status, update_klipperscreen
from components.moonraker.services.moonraker_setup_service import MoonrakerSetupService
from components.moonraker.utils.utils import get_moonraker_status
from components.webui_client.client_config.client_config_setup import update_client_config
from components.webui_client.client_setup import update_client
from components.webui_client.client_utils import get_client_config_status, get_client_status
from components.webui_client.fluidd_data import FluiddData
from components.webui_client.mainsail_data import MainsailData
from core.logger import DialogType, Logger
from core.menus import Option
from core.menus.base_menu import BaseMenu
from core.types.color import Color
from core.types.component_status import ComponentStatus
from utils.input_utils import get_confirm
from utils.sys_utils import get_upgradable_packages, update_system_package_lists, upgrade_system_packages

class UpdateMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None) -> None:
        super().__init__()
        self.loading_msg = translate('loading_update_menu_please_wait_8e9730')
        self.is_loading(True)
        self.title = translate('update_menu_79bee1')
        self.title_color = Color.GREEN
        self.previous_menu: Type[BaseMenu] | None = previous_menu
        self.packages: List[str] = []
        self.package_count: int = 0
        self.klipper_local = self.klipper_remote = ''
        self.moonraker_local = self.moonraker_remote = ''
        self.mainsail_local = self.mainsail_remote = ''
        self.mainsail_config_local = self.mainsail_config_remote = ''
        self.fluidd_local = self.fluidd_remote = ''
        self.fluidd_config_local = self.fluidd_config_remote = ''
        self.klipperscreen_local = self.klipperscreen_remote = ''
        self.crowsnest_local = self.crowsnest_remote = ''
        self.mainsail_data = MainsailData()
        self.fluidd_data = FluiddData()
        self.status_data = {'klipper': {'display_name': 'Klipper', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'moonraker': {'display_name': 'Moonraker', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'mainsail': {'display_name': 'Mainsail', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'mainsail_config': {'display_name': 'Mainsail-Config', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'fluidd': {'display_name': 'Fluidd', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'fluidd_config': {'display_name': 'Fluidd-Config', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'klipperscreen': {'display_name': 'KlipperScreen', translate('installed_85841a'): False, 'local': None, 'remote': None}, 'crowsnest': {'display_name': 'Crowsnest', translate('installed_85841a'): False, 'local': None, 'remote': None}}
        self._fetch_update_status()
        self.is_loading(False)

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from core.menus.main_menu import MainMenu
        self.previous_menu = previous_menu if previous_menu is not None else MainMenu

    def set_options(self) -> None:
        self.options = {'a': Option(self.update_all), '1': Option(self.update_klipper), '2': Option(self.update_moonraker), '3': Option(self.update_mainsail), '4': Option(self.update_fluidd), '5': Option(self.update_mainsail_config), '6': Option(self.update_fluidd_config), '7': Option(self.update_klipperscreen), '8': Option(self.update_crowsnest), '9': Option(self.upgrade_system_packages)}

    def print_menu(self) -> None:
        sysupgrades: str = 'No upgrades available.'
        padding = 29
        if self.package_count > 0:
            sysupgrades = Color.apply(f'{self.package_count} upgrades available!', Color.GREEN)
            padding = 38
        menu = textwrap.dedent(f'\n            ╟───────────────────────┬───────────────┬───────────────╢\n            ║  a) Update all        │               │               ║\n            ║                       │ Current:      │ Latest:       ║\n            ║ Klipper & API:        ├───────────────┼───────────────╢\n            ║  1) Klipper           │ {self.klipper_local:<22} │ {self.klipper_remote:<22} ║\n            ║  2) Moonraker         │ {self.moonraker_local:<22} │ {self.moonraker_remote:<22} ║\n            ║                       │               │               ║\n            ║ Webinterface:         ├───────────────┼───────────────╢\n            ║  3) Mainsail          │ {self.mainsail_local:<22} │ {self.mainsail_remote:<22} ║\n            ║  4) Fluidd            │ {self.fluidd_local:<22} │ {self.fluidd_remote:<22} ║\n            ║                       │               │               ║\n            ║ Client-Config:        ├───────────────┼───────────────╢\n            ║  5) Mainsail-Config   │ {self.mainsail_config_local:<22} │ {self.mainsail_config_remote:<22} ║\n            ║  6) Fluidd-Config     │ {self.fluidd_config_local:<22} │ {self.fluidd_config_remote:<22} ║\n            ║                       │               │               ║\n            ║ Other:                ├───────────────┼───────────────╢\n            ║  7) KlipperScreen     │ {self.klipperscreen_local:<22} │ {self.klipperscreen_remote:<22} ║\n            ║  8) Crowsnest         │ {self.crowsnest_local:<22} │ {self.crowsnest_remote:<22} ║\n            ║                       ├───────────────┴───────────────╢\n            ║  9) System            │ {sysupgrades:^{padding}} ║\n            ╟───────────────────────┴───────────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def update_all(self, **kwargs) -> None:
        Logger.print_status(translate('updating_all_components_236acf'))
        self.update_klipper()
        self.update_moonraker()
        self.update_mainsail()
        self.update_mainsail_config()
        self.update_fluidd()
        self.update_fluidd_config()
        self.update_klipperscreen()
        self.update_crowsnest()
        self.upgrade_system_packages()

    def update_klipper(self, **kwargs) -> None:
        klsvc = KlipperSetupService()
        self._run_update_routine('klipper', klsvc.update)

    def update_moonraker(self, **kwargs) -> None:
        mrsvc = MoonrakerSetupService()
        self._run_update_routine('moonraker', mrsvc.update)

    def update_mainsail(self, **kwargs) -> None:
        self._run_update_routine('mainsail', update_client, self.mainsail_data)

    def update_mainsail_config(self, **kwargs) -> None:
        self._run_update_routine('mainsail_config', update_client_config, self.mainsail_data)

    def update_fluidd(self, **kwargs) -> None:
        self._run_update_routine('fluidd', update_client, self.fluidd_data)

    def update_fluidd_config(self, **kwargs) -> None:
        self._run_update_routine('fluidd_config', update_client_config, self.fluidd_data)

    def update_klipperscreen(self, **kwargs) -> None:
        self._run_update_routine('klipperscreen', update_klipperscreen)

    def update_crowsnest(self, **kwargs) -> None:
        self._run_update_routine('crowsnest', update_crowsnest)

    def upgrade_system_packages(self, **kwargs) -> None:
        self._run_system_updates()

    def _fetch_update_status(self) -> None:
        self._set_status_data('klipper', get_klipper_status)
        self._set_status_data('moonraker', get_moonraker_status)
        self._set_status_data('mainsail', get_client_status, self.mainsail_data, True)
        self._set_status_data('mainsail_config', get_client_config_status, self.mainsail_data)
        self._set_status_data('fluidd', get_client_status, self.fluidd_data, True)
        self._set_status_data('fluidd_config', get_client_config_status, self.fluidd_data)
        self._set_status_data('klipperscreen', get_klipperscreen_status)
        self._set_status_data('crowsnest', get_crowsnest_status)
        update_system_package_lists(silent=True)
        self.packages = get_upgradable_packages()
        self.package_count = len(self.packages)

    def _format_local_status(self, local_version, remote_version) -> str:
        color = Color.RED
        if not local_version:
            color = Color.RED
        elif local_version == remote_version:
            color = Color.GREEN
        elif local_version != remote_version:
            color = Color.YELLOW
        return Color.apply(local_version or '-', color)

    def _set_status_data(self, name: str, status_fn: Callable, *args) -> None:
        comp_status: ComponentStatus = status_fn(*args)
        self.status_data[name][translate('installed_85841a')] = True if comp_status.status == 2 else False
        self.status_data[name]['local'] = comp_status.local
        self.status_data[name]['remote'] = comp_status.remote
        self._set_status_string(name)

    def _set_status_string(self, name: str) -> None:
        local_status = self.status_data[name].get('local', None)
        remote_status = self.status_data[name].get('remote', None)
        color = Color.GREEN if remote_status else Color.RED
        local_txt = self._format_local_status(local_status, remote_status)
        remote_txt = Color.apply(remote_status or '-', color)
        setattr(self, f'{name}_local', local_txt)
        setattr(self, f'{name}_remote', remote_txt)

    def _check_is_installed(self, name: str) -> bool:
        return self.status_data[name][translate('installed_85841a')]

    def _is_update_available(self, name: str) -> bool:
        return self.status_data[name]['local'] != self.status_data[name]['remote']

    def _run_update_routine(self, name: str, update_fn: Callable, *args) -> None:
        display_name = self.status_data[name]['display_name']
        is_installed = self._check_is_installed(name)
        is_update_available = self._is_update_available(name)
        if not is_installed:
            Logger.print_info(f'{display_name} is not installed! Skipped ...')
            return
        elif not is_update_available:
            Logger.print_info(f'{display_name} is already up to date! Skipped ...')
            return
        update_fn(*args)

    def _run_system_updates(self) -> None:
        if not self.packages:
            Logger.print_info(translate('no_system_upgrades_available_324b07'))
            return
        try:
            pkgs: str = ', '.join(self.packages)
            Logger.print_dialog(DialogType.CUSTOM, ['The following packages will be upgraded:', '\n\n', pkgs], custom_title=translate('upgradable_system_updates_74b9a7'))
            if not get_confirm('Continue?'):
                return
            Logger.print_status(translate('upgrading_system_packages_dc90ad'))
            upgrade_system_packages(self.packages)
        except Exception as e:
            Logger.print_error(f'Error upgrading system packages:\n{e}')
            raise