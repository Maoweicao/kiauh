import textwrap
from typing import List
from components.klipper.klipper import Klipper
from components.moonraker.moonraker import Moonraker
from core.menus.base_menu import print_back_footer
from core.types.color import Color

def print_moonraker_overview(klipper_instances: List[Klipper], moonraker_instances: List[Moonraker], show_index=False, show_select_all=False):
    headline = Color.apply(translate('the_following_instances_were_found_5906ec'), Color.GREEN)
    dialog = textwrap.dedent(f'\n        ╔═══════════════════════════════════════════════════════╗\n        ║{headline:^64}║\n        ╟───────────────────────────────────────────────────────╢\n        ')[1:]
    if show_select_all:
        select_all = Color.apply('a) Select all', Color.YELLOW)
        dialog += f'║ {select_all:<63}║\n'
        dialog += '║                                                       ║\n'
    instance_map = {k.service_file_path.stem: k.service_file_path.stem.replace('klipper', 'moonraker') if k.suffix in [m.suffix for m in moonraker_instances] else '' for k in klipper_instances}
    for i, k in enumerate(instance_map):
        mr_name = instance_map.get(k)
        m = f'<-> {mr_name}' if mr_name != '' else ''
        line = Color.apply(f"{(f'{i + 1})' if show_index else '●')} {k} {m}", Color.CYAN)
        dialog += f'║ {line:<63}║\n'
    warn_l1 = Color.apply(translate('please_note_195ae8'), Color.YELLOW)
    warn_l2 = Color.apply(translate('if_you_select_an_instance_f0776b'), Color.YELLOW)
    warn_l3 = Color.apply('instance, that Moonraker instance will be re-created!', Color.YELLOW)
    warning = textwrap.dedent(f'\n        ║                                                       ║\n        ╟───────────────────────────────────────────────────────╢\n        ║ {warn_l1:<63}║\n        ║ {warn_l2:<63}║\n        ║ {warn_l3:<63}║\n        ╟───────────────────────────────────────────────────────╢\n        ')[1:]
    dialog += warning
    print(dialog, end='')
    print_back_footer()