from __future__ import annotations
import textwrap
from typing import Tuple, Type
from core.menus.base_menu import BaseMenu, MenuTitleStyle
from core.types.color import Color

def __title_config__() -> Tuple[str, Color, MenuTitleStyle]:
    return ('< ? > Help: Flash MCU < ? >', Color.YELLOW, MenuTitleStyle.PLAIN)

class KlipperFlashMethodHelpMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title, self.title_color, self.title_style = __title_config__()
        self.previous_menu: Type[BaseMenu] | None = previous_menu

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from components.klipper_firmware.menus.klipper_flash_menu import KlipperFlashMethodMenu
        self.previous_menu = previous_menu if previous_menu is not None else KlipperFlashMethodMenu

    def set_options(self) -> None:
        pass

    def print_menu(self) -> None:
        subheader1 = Color.apply('Regular flashing method:', Color.CYAN)
        subheader2 = Color.apply(translate('updating_via_sdcard_update_ac2ebc'), Color.CYAN)
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ {subheader1:<62} ║\n            ║ The default method to flash controller boards which   ║\n            ║ are connected and updated over USB and not by placing ║\n            ║ a compiled firmware file onto an internal SD-Card.    ║\n            ║                                                       ║\n            ║ Common controllers that get flashed that way are:     ║\n            ║ - Arduino Mega 2560                                   ║\n            ║ - Fysetc F6 / S6 (used without a Display + SD-Slot)   ║\n            ║                                                       ║\n            ║ {subheader2:<62} ║\n            ║ Many popular controller boards ship with a bootloader ║\n            ║ capable of updating the firmware via SD-Card.         ║\n            ║ Choose this method if your controller board supports  ║\n            ║ this way of updating. This method ONLY works for up-  ║\n            ║ grading firmware. The initial flashing procedure must ║\n            ║ be done manually per the instructions that apply to   ║\n            ║ your controller board.                                ║\n            ║                                                       ║\n            ║ Common controllers that can be flashed that way are:  ║\n            ║ - BigTreeTech SKR 1.3 / 1.4 (Turbo) / E3 / Mini E3    ║\n            ║ - Fysetc F6 / S6 (used with a Display + SD-Slot)      ║\n            ║ - Fysetc Spider                                       ║\n            ║                                                       ║\n            ╟───────────────────────────────────────────────────────╢\n            ')[1:]
        print(menu, end='')

class KlipperFlashCommandHelpMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title, self.title_color, self.title_style = __title_config__()
        self.previous_menu: Type[BaseMenu] | None = previous_menu

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from components.klipper_firmware.menus.klipper_flash_menu import KlipperFlashCommandMenu
        self.previous_menu = previous_menu if previous_menu is not None else KlipperFlashCommandMenu

    def set_options(self) -> None:
        pass

    def print_menu(self) -> None:
        subheader1 = Color.apply('make flash:', Color.CYAN)
        subheader2 = Color.apply('make serialflash:', Color.CYAN)
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ {subheader1:<62} ║\n            ║ The default command to flash controller board, it     ║\n            ║ will detect selected microcontroller and use suitable ║\n            ║ tool for flashing it.                                 ║\n            ║                                                       ║\n            ║ {subheader2:<62} ║\n            ║ Special command to flash STM32 microcontrollers in    ║\n            ║ DFU mode but connected via serial. stm32flash command ║\n            ║ will be used internally.                              ║\n            ║                                                       ║\n            ')[1:]
        print(menu, end='')

class KlipperMcuConnectionHelpMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title, self.title_color, self.title_style = __title_config__()
        self.previous_menu: Type[BaseMenu] | None = previous_menu

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from components.klipper_firmware.menus.klipper_flash_menu import KlipperSelectMcuConnectionMenu
        self.previous_menu = previous_menu if previous_menu is not None else KlipperSelectMcuConnectionMenu

    def set_options(self) -> None:
        pass

    def print_menu(self) -> None:
        subheader1 = Color.apply('USB:', Color.CYAN)
        subheader2 = Color.apply('UART:', Color.CYAN)
        subheader3 = Color.apply('USB DFU:', Color.CYAN)
        subheader4 = Color.apply('USB RP2040 Boot:', Color.CYAN)
        menu = textwrap.dedent(f"\n            ╟───────────────────────────────────────────────────────╢\n            ║ {subheader1:<62} ║\n            ║ Selecting USB as the connection method will scan the  ║\n            ║ USB ports for connected controller boards. This will  ║\n            ║ be similar to the 'ls /dev/serial/by-id/*' command    ║\n            ║ suggested by the official Klipper documentation for   ║\n            ║ determining successfull USB connections!              ║\n            ║                                                       ║\n            ║ {subheader2:<62} ║\n            ║ Selecting UART as the connection method will list all ║\n            ║ possible UART serial ports. Note: This method ALWAYS  ║\n            ║ returns something as it seems impossible to determine ║\n            ║ if a valid Klipper controller board is connected or   ║\n            ║ not. Because of that, you MUST know which UART serial ║\n            ║ port your controller board is connected to when using ║\n            ║ this connection method.                               ║\n            ║                                                       ║\n            ║ {subheader3:<62} ║\n            ║ Selecting USB DFU as the connection method will scan  ║\n            ║ the USB ports for connected controller boards in      ║\n            ║ STM32 DFU mode, which is usually done by holding down ║\n            ║ the BOOT button or setting a special jumper on the    ║\n            ║ board before powering up.                             ║\n            ║                                                       ║\n            ║ {subheader4:<62} ║\n            ║ Selecting USB RP2 Boot as the connection method will  ║\n            ║ scan the USB ports for connected RP2040 controller    ║\n            ║ boards in Boot mode, which is usually done by holding ║\n            ║ down the BOOT button before powering up.              ║\n            ║                                                       ║\n            ╟───────────────────────────────────────────────────────╢\n            ")[1:]
        print(menu, end='')