from __future__ import annotations
import shutil
import time
from pathlib import Path
from subprocess import CalledProcessError, run
from typing import List
from components.crowsnest import CROWSNEST_BACKUP_DIR, CROWSNEST_BIN_FILE, CROWSNEST_DIR, CROWSNEST_INSTALL_SCRIPT, CROWSNEST_LOGROTATE_FILE, CROWSNEST_MULTI_CONFIG, CROWSNEST_REPO, CROWSNEST_SERVICE_FILE, CROWSNEST_SERVICE_NAME
from components.klipper.klipper import Klipper
from core.backup_manager.backup_manager import BackupManager
from core.logger import DialogType, Logger
from core.settings.kiauh_settings import KiauhSettings
from core.types.component_status import ComponentStatus
from utils.common import check_install_dependencies, get_install_status
from utils.git_utils import git_clone_wrapper, git_pull_wrapper
from utils.input_utils import get_confirm
from utils.instance_utils import get_instances
from utils.sys_utils import cmd_sysctl_service, parse_packages_from_file

def install_crowsnest() -> None:
    git_clone_wrapper(CROWSNEST_REPO, CROWSNEST_DIR, 'master')
    check_install_dependencies({'make'})
    instances: List[Klipper] = get_instances(Klipper)
    if len(instances) > 1:
        print_multi_instance_warning(instances)
        if not get_confirm('Do you want to continue with the installation?'):
            Logger.print_info(translate('crowsnest_installation_aborted_02df45'))
            return
        Logger.print_status(translate('launching_crowsnests_install_configurator_86fb7e'))
        time.sleep(3)
        configure_multi_instance()
    Logger.print_status(translate('launching_crowsnest_installer_4183b5'))
    Logger.print_info(translate('installer_will_prompt_you_for_cfd00d'))
    try:
        run('sudo make install', cwd=CROWSNEST_DIR, shell=True, check=True)
    except CalledProcessError as e:
        Logger.print_error(f'Something went wrong! Please try again...\n{e}')
        return

def print_multi_instance_warning(instances: List[Klipper]) -> None:
    Logger.print_dialog(DialogType.WARNING, [translate('multi_instance_install_detected_6ceb1e'), '\n\n', "Crowsnest is NOT designed to support multi instances. A workaround for this is to choose the most used instance as a 'master' and use this instance to set up your 'crowsnest.conf' and steering it's service.", '\n\n', translate('the_following_instances_were_found_5906ec'), *[f'● {instance.data_dir.name}' for instance in instances]])

def configure_multi_instance() -> None:
    try:
        run('make config', cwd=CROWSNEST_DIR, shell=True, check=True)
    except CalledProcessError as e:
        Logger.print_error(f'Something went wrong! Please try again...\n{e}')
        if CROWSNEST_MULTI_CONFIG.exists():
            Path.unlink(CROWSNEST_MULTI_CONFIG)
        return
    if not CROWSNEST_MULTI_CONFIG.exists():
        Logger.print_error(translate('generating_config_failed_installation_aborted_c7c258'))

def update_crowsnest() -> None:
    try:
        cmd_sysctl_service(CROWSNEST_SERVICE_NAME, 'stop')
        if not CROWSNEST_DIR.exists():
            git_clone_wrapper(CROWSNEST_REPO, CROWSNEST_DIR, 'master')
        else:
            Logger.print_status(translate('updating_crowsnest_2fefd0'))
            settings = KiauhSettings()
            if settings.kiauh.backup_before_update:
                bm = BackupManager()
                bm.backup_directory(CROWSNEST_DIR.name, source=CROWSNEST_DIR, target=CROWSNEST_BACKUP_DIR)
            git_pull_wrapper(CROWSNEST_DIR)
            deps = parse_packages_from_file(CROWSNEST_INSTALL_SCRIPT)
            check_install_dependencies({*deps})
        cmd_sysctl_service(CROWSNEST_SERVICE_NAME, 'restart')
        Logger.print_ok(translate('crowsnest_updated_successfully_79eeca'), end='\n\n')
    except CalledProcessError as e:
        Logger.print_error(f'Something went wrong! Please try again...\n{e}')
        return

def get_crowsnest_status() -> ComponentStatus:
    files = [CROWSNEST_BIN_FILE, CROWSNEST_LOGROTATE_FILE, CROWSNEST_SERVICE_FILE]
    return get_install_status(CROWSNEST_DIR, files=files)

def remove_crowsnest() -> None:
    if not CROWSNEST_DIR.exists():
        Logger.print_info(translate('crowsnest_does_not_seem_to_f0d78b'))
        return
    try:
        run(translate('make_uninstall_b2e5d8'), cwd=CROWSNEST_DIR, shell=True, check=True)
    except CalledProcessError as e:
        Logger.print_error(f'Something went wrong! Please try again...\n{e}')
        return
    Logger.print_status(translate('removing_crowsnest_directory_6a3d9a'))
    shutil.rmtree(CROWSNEST_DIR)
    Logger.print_ok(translate('directory_removed_a43181'))