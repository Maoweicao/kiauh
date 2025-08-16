from __future__ import annotations
import textwrap
from typing import Type
from components.klipper_firmware.flash_options import FlashMethod, FlashOptions
from core.menus import FooterType, Option
from core.menus.base_menu import BaseMenu, MenuTitleStyle
from core.types.color import Color

class KlipperNoFirmwareErrorMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = translate('no_firmware_file_found_02fa82')
        self.title_color = Color.RED
        self.title_style = MenuTitleStyle.PLAIN
        self.previous_menu: Type[BaseMenu] | None = previous_menu
        self.flash_options = FlashOptions()
        self.footer_type = FooterType.BLANK
        self.input_label_txt = 'Press ENTER to go back to [Advanced Menu]'

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu

    def set_options(self) -> None:
        self.default_option = Option(method=self.go_back)

    def print_menu(self) -> None:
        line1 = 'Unable to find a compiled firmware file!'
        menu = textwrap.dedent(f"\n            ╟───────────────────────────────────────────────────────╢\n            ║ {Color.apply(line1, Color.RED):<62} ║\n            ║                                                       ║\n            ║ Make sure, that:                                      ║\n            ║ ● the folder '~/klipper/out' and its content exist    ║\n            ║ ● the folder contains the following file:             ║\n            ")[1:]
        if self.flash_options.flash_method is FlashMethod.REGULAR:
            menu += "║   ● 'klipper.elf'                                     ║\n"
            menu += "║   ● 'klipper.elf.hex'                                 ║\n"
        else:
            menu += "║   ● 'klipper.bin'                                     ║\n"
        print(menu, end='')

    def go_back(self, **kwargs) -> None:
        from core.menus.advanced_menu import AdvancedMenu
        AdvancedMenu().run()

class KlipperNoBoardTypesErrorMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = translate('error_getting_board_list_ff15fc')
        self.title_color = Color.RED
        self.title_style = MenuTitleStyle.PLAIN
        self.previous_menu: Type[BaseMenu] | None = previous_menu
        self.footer_type = FooterType.BLANK
        self.input_label_txt = 'Press ENTER to go back to [Main Menu]'

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu

    def set_options(self) -> None:
        self.default_option = Option(method=self.go_back)

    def print_menu(self) -> None:
        line1 = translate('reading_the_list_of_supported_3b6fa8')
        menu = textwrap.dedent(f"\n            ╟───────────────────────────────────────────────────────╢\n            ║ {Color.apply(line1, Color.RED):<62} ║\n            ║                                                       ║\n            ║ Make sure, that:                                      ║\n            ║ ● the folder '~/klipper' and all its content exist    ║\n            ║ ● the content of folder '~/klipper' is not currupted  ║\n            ║ ● the file '~/klipper/scripts/flash-sd.py' exist      ║\n            ║ ● your current user has access to those files/folders ║\n            ║                                                       ║\n            ║ If in doubt or this process continues to fail, please ║\n            ║ consider to download Klipper again.                   ║\n            ")[1:]
        print(menu, end='')

    def go_back(self, **kwargs) -> None:
        from core.menus.main_menu import MainMenu
        MainMenu().run()