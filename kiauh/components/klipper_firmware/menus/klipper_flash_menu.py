from __future__ import annotations
import textwrap
import time
from pathlib import Path
from typing import Type
from components.klipper_firmware.firmware_utils import find_firmware_file, find_uart_device, find_usb_device_by_id, find_usb_dfu_device, find_usb_rp2_boot_device, get_sd_flash_board_list, start_flash_process
from components.klipper_firmware.flash_options import ConnectionType, FlashCommand, FlashMethod, FlashOptions
from components.klipper_firmware.menus.klipper_flash_error_menu import KlipperNoBoardTypesErrorMenu, KlipperNoFirmwareErrorMenu
from components.klipper_firmware.menus.klipper_flash_help_menu import KlipperFlashCommandHelpMenu, KlipperFlashMethodHelpMenu, KlipperMcuConnectionHelpMenu
from core.logger import DialogType, Logger
from core.menus import FooterType, Option
from core.menus.base_menu import BaseMenu, MenuTitleStyle
from core.types.color import Color
from utils.input_utils import get_number_input

class KlipperFlashMethodMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = 'MCU Flash Menu'
        self.title_color = Color.CYAN
        self.help_menu = KlipperFlashMethodHelpMenu
        self.input_label_txt = 'Select flash method'
        self.footer_type = FooterType.BACK_HELP
        self.flash_options = FlashOptions()

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        from core.menus.advanced_menu import AdvancedMenu
        self.previous_menu = previous_menu if previous_menu is not None else AdvancedMenu

    def set_options(self) -> None:
        self.options = {'1': Option(self.select_regular), '2': Option(self.select_sdcard)}

    def print_menu(self) -> None:
        subheader = Color.apply('ATTENTION:', Color.YELLOW)
        subline1 = Color.apply('Make sure to select the correct method for the MCU!', Color.YELLOW)
        subline2 = Color.apply('Not all MCUs support both methods!', Color.YELLOW)
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ Select the flash method for flashing the MCU.         ║\n            ║                                                       ║\n            ║ {subheader:<62} ║\n            ║ {subline1:<62} ║\n            ║ {subline2:<62} ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ 1) Regular flashing method                            ║\n            ║ 2) Updating via SD-Card Update                        ║\n            ╟───────────────────────────┬───────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def select_regular(self, **kwargs):
        self.flash_options.flash_method = FlashMethod.REGULAR
        self.goto_next_menu()

    def select_sdcard(self, **kwargs):
        self.flash_options.flash_method = FlashMethod.SD_CARD
        self.goto_next_menu()

    def goto_next_menu(self, **kwargs):
        if find_firmware_file():
            KlipperFlashCommandMenu(previous_menu=self.__class__).run()
        else:
            KlipperNoFirmwareErrorMenu().run()

class KlipperFlashCommandMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = 'Which flash command to use for flashing the MCU?'
        self.title_style = MenuTitleStyle.PLAIN
        self.title_color = Color.YELLOW
        self.help_menu = KlipperFlashCommandHelpMenu
        self.input_label_txt = 'Select flash command'
        self.footer_type = FooterType.BACK_HELP
        self.flash_options = FlashOptions()

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu if previous_menu is not None else KlipperFlashMethodMenu

    def set_options(self) -> None:
        self.options = {'1': Option(self.select_flash), '2': Option(self.select_serialflash)}
        self.default_option = Option(self.select_flash)

    def print_menu(self) -> None:
        menu = textwrap.dedent('\n            ╟───────────────────────────────────────────────────────╢\n            ║ 1) make flash (default)                               ║\n            ║ 2) make serialflash (stm32flash)                      ║\n            ╟───────────────────────────┬───────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def select_flash(self, **kwargs):
        self.flash_options.flash_command = FlashCommand.FLASH
        self.goto_next_menu()

    def select_serialflash(self, **kwargs):
        self.flash_options.flash_command = FlashCommand.SERIAL_FLASH
        self.goto_next_menu()

    def goto_next_menu(self, **kwargs):
        KlipperSelectMcuConnectionMenu(previous_menu=self.__class__).run()

class KlipperSelectMcuConnectionMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None, standalone: bool=False):
        super().__init__()
        self.title = 'Make sure that the controller board is connected now!'
        self.title_style = MenuTitleStyle.PLAIN
        self.title_color = Color.YELLOW
        self.previous_menu: Type[BaseMenu] | None = previous_menu
        self.__standalone = standalone
        self.help_menu = KlipperMcuConnectionHelpMenu
        self.input_label_txt = translate('select_connection_type_5684b1')
        self.footer_type = FooterType.BACK_HELP
        self.flash_options = FlashOptions()

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu if previous_menu is not None else KlipperFlashCommandMenu

    def set_options(self) -> None:
        self.options = {'1': Option(method=self.select_usb), '2': Option(method=self.select_dfu), '3': Option(method=self.select_usb_dfu), '4': Option(method=self.select_usb_rp2040)}

    def print_menu(self) -> None:
        menu = textwrap.dedent('\n            ╟───────────────────────────────────────────────────────╢\n            ║ How is the controller board connected to the host?    ║\n            ╟───────────────────────────────────────────────────────╢\n            ║ 1) USB                                                ║\n            ║ 2) UART                                               ║\n            ║ 3) USB (DFU mode)                                     ║\n            ║ 4) USB (RP2040 mode)                                  ║\n            ╟───────────────────────────┬───────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def select_usb(self, **kwargs):
        self.flash_options.connection_type = ConnectionType.USB
        self.get_mcu_list()

    def select_dfu(self, **kwargs):
        self.flash_options.connection_type = ConnectionType.UART
        self.get_mcu_list()

    def select_usb_dfu(self, **kwargs):
        self.flash_options.connection_type = ConnectionType.USB_DFU
        self.get_mcu_list()

    def select_usb_rp2040(self, **kwargs):
        self.flash_options.connection_type = ConnectionType.USB_RP2040
        self.get_mcu_list()

    def get_mcu_list(self, **kwargs):
        conn_type = self.flash_options.connection_type
        if conn_type is ConnectionType.USB:
            Logger.print_status(translate('identifying_mcu_connected_via_usb_20c88d'))
            self.flash_options.mcu_list = find_usb_device_by_id()
        elif conn_type is ConnectionType.UART:
            Logger.print_status(translate('identifying_mcu_possibly_connected_via_b3d4b0'))
            self.flash_options.mcu_list = find_uart_device()
        elif conn_type is ConnectionType.USB_DFU:
            Logger.print_status(translate('identifying_mcu_connected_via_usb_b2377f'))
            self.flash_options.mcu_list = find_usb_dfu_device()
        elif conn_type is ConnectionType.USB_RP2040:
            Logger.print_status(translate('identifying_mcu_connected_via_usb_4c75fd'))
            self.flash_options.mcu_list = find_usb_rp2_boot_device()
        if len(self.flash_options.mcu_list) < 1:
            Logger.print_warn(translate('no_mcus_found_167fdd'))
            Logger.print_warn(translate('make_sure_they_are_connected_05432d'))
        if self.__standalone and len(self.flash_options.mcu_list) > 0:
            Logger.print_ok(translate('the_following_mcus_were_found_1d2b3e'), prefix=False)
            for i, mcu in enumerate(self.flash_options.mcu_list):
                print(f'   ● MCU #{i}: {Color.CYAN}{mcu}{Color.RST}')
            time.sleep(3)
            return
        self.goto_next_menu()

    def goto_next_menu(self, **kwargs):
        KlipperSelectMcuIdMenu(previous_menu=self.__class__).run()

class KlipperSelectMcuIdMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = '!!! ATTENTION !!!'
        self.title_style = MenuTitleStyle.PLAIN
        self.title_color = Color.RED
        self.flash_options = FlashOptions()
        self.mcu_list = self.flash_options.mcu_list
        self.input_label_txt = 'Select MCU to flash'
        self.footer_type = FooterType.BACK

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu if previous_menu is not None else KlipperSelectMcuConnectionMenu

    def set_options(self) -> None:
        self.options = {f'{i}': Option(self.flash_mcu, f'{i}') for i in range(len(self.mcu_list))}

    def print_menu(self) -> None:
        header2 = f"[{Color.apply(translate('list_of_detected_mcus_4c0f0a'), Color.CYAN)}]"
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ Make sure, to select the correct MCU!                 ║\n            ║ ONLY flash a firmware created for the respective MCU! ║\n            ║                                                       ║\n            ╟{header2:─^64}╢\n            ║                                                       ║\n            ')[1:]
        for i, mcu in enumerate(self.mcu_list):
            mcu = mcu.split('/')[-1]
            menu += f"║ {i}) {Color.apply(f'{mcu:<51}', Color.CYAN)}║\n"
        menu += textwrap.dedent('\n            ║                                                       ║\n            ╟───────────────────────────────────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def flash_mcu(self, **kwargs):
        try:
            index: int | None = kwargs.get('opt_index', None)
            if index is None:
                raise Exception('opt_index is None')
            index = int(index)
            selected_mcu = self.mcu_list[index]
            self.flash_options.selected_mcu = selected_mcu
            if self.flash_options.flash_method == FlashMethod.SD_CARD:
                KlipperSelectSDFlashBoardMenu(previous_menu=self.__class__).run()
            elif self.flash_options.flash_method == FlashMethod.REGULAR:
                KlipperFlashOverviewMenu(previous_menu=self.__class__).run()
        except Exception as e:
            Logger.print_error(e)
            Logger.print_error(translate('flashing_failed_08aa70'))

class KlipperSelectSDFlashBoardMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.flash_options = FlashOptions()
        self.available_boards = get_sd_flash_board_list()
        self.input_label_txt = 'Select board type'

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu = previous_menu if previous_menu is not None else KlipperSelectMcuIdMenu

    def set_options(self) -> None:
        self.options = {f'{i}': Option(self.board_select, f'{i}') for i in range(len(self.available_boards))}

    def print_menu(self) -> None:
        if len(self.available_boards) < 1:
            KlipperNoBoardTypesErrorMenu().run()
        else:
            menu = textwrap.dedent('\n                ║ Please select the type of board that corresponds to   ║\n                ║ the currently selected MCU ID you chose before.       ║\n                ║                                                       ║\n                ║ The following boards are currently supported:         ║\n                ╟───────────────────────────────────────────────────────╢\n                ')[1:]
            for i, board in enumerate(self.available_boards):
                line = f' {i}) {board}'
                menu += f'║{line:<55}║\n'
            menu += '╟───────────────────────────────────────────────────────╢'
            print(menu, end='')

    def board_select(self, **kwargs):
        try:
            index: int | None = kwargs.get('opt_index', None)
            if index is None:
                raise Exception('opt_index is None')
            index = int(index)
            self.flash_options.selected_board = self.available_boards[index]
            self.baudrate_select()
        except Exception as e:
            Logger.print_error(e)
            Logger.print_error(translate('board_selection_failed_d4fe58'))

    def baudrate_select(self, **kwargs):
        Logger.print_dialog(DialogType.CUSTOM, ['If your board is flashed with firmware that connects at a custom baud rate, please change it now.', '\n\n', 'If you are unsure, stick to the default 250000!'])
        self.flash_options.selected_baudrate = get_number_input(question=translate('please_set_the_baud_rate_46bfa5'), default=250000, min_value=0, allow_go_back=True)
        KlipperFlashOverviewMenu(previous_menu=self.__class__).run()

class KlipperFlashOverviewMenu(BaseMenu):

    def __init__(self, previous_menu: Type[BaseMenu] | None=None):
        super().__init__()
        self.title = '!!! ATTENTION !!!'
        self.title_style = MenuTitleStyle.PLAIN
        self.title_color = Color.RED
        self.flash_options = FlashOptions()
        self.input_label_txt = 'Perform action (default=Y)'

    def set_previous_menu(self, previous_menu: Type[BaseMenu] | None) -> None:
        self.previous_menu: Type[BaseMenu] | None = previous_menu

    def set_options(self) -> None:
        self.options = {'y': Option(self.execute_flash), 'n': Option(self.abort_process)}
        self.default_option = Option(self.execute_flash)

    def print_menu(self) -> None:
        method = self.flash_options.flash_method.value
        command = self.flash_options.flash_command.value
        conn_type = self.flash_options.connection_type.value
        mcu = self.flash_options.selected_mcu.split('/')[-1]
        board = self.flash_options.selected_board
        baudrate = self.flash_options.selected_baudrate
        kconfig = Path(self.flash_options.selected_kconfig).name
        color = Color.CYAN
        subheader = f"[{Color.apply('Overview', color)}]"
        menu = textwrap.dedent(f'\n            ╟───────────────────────────────────────────────────────╢\n            ║ Before contuining the flashing process, please check  ║\n            ║ if all parameters were set correctly! Once you made   ║\n            ║ sure everything is correct, start the process. If any ║\n            ║ parameter needs to be changed, you can go back (B)    ║\n            ║ step by step or abort and start from the beginning.   ║\n            ║{subheader:─^64}║\n            ║                                                       ║\n            ')[1:]
        menu += textwrap.dedent(f"\n            ║ MCU: {Color.apply(f'{mcu:<48}', color)} ║\n            ║ Connection: {Color.apply(f'{conn_type:<41}', color)} ║\n            ║ Flash method: {Color.apply(f'{method:<39}', color)} ║\n            ║ Flash command: {Color.apply(f'{command:<38}', color)} ║\n            ")[1:]
        if self.flash_options.flash_method is FlashMethod.SD_CARD:
            menu += textwrap.dedent(f"\n                ║ Board type: {Color.apply(f'{board:<41}', color)} ║\n                ║ Baudrate: {Color.apply(f'{baudrate:<43}', color)} ║\n                ")[1:]
        if self.flash_options.flash_method is FlashMethod.REGULAR:
            menu += textwrap.dedent(f"\n                ║ Firmware config: {Color.apply(f'{kconfig:<36}', color)} ║\n                ")[1:]
        menu += textwrap.dedent('\n            ║                                                       ║\n            ╟───────────────────────────────────────────────────────╢\n            ║  Y) Start flash process                               ║\n            ║  N) Abort - Return to Advanced Menu                   ║\n            ╟───────────────────────────────────────────────────────╢\n            ')[1:]
        print(menu, end='')

    def execute_flash(self, **kwargs):
        start_flash_process(self.flash_options)
        Logger.print_info(translate('returning_to_mcu_flash_menu_354390'))
        time.sleep(5)
        KlipperFlashMethodMenu().run()

    def abort_process(self, **kwargs):
        from core.menus.advanced_menu import AdvancedMenu
        AdvancedMenu().run()