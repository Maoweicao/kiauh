import json
from typing import List
from components.klipper.klipper import Klipper
from components.moonraker.moonraker import Moonraker
from core.instance_manager.instance_manager import InstanceManager
from core.logger import DialogType, Logger
from extensions.base_extension import BaseExtension
from extensions.octoapp import OA_DEPS_JSON_FILE, OA_DIR, OA_ENV_DIR, OA_INSTALL_SCRIPT, OA_INSTALLER_LOG_FILE, OA_REPO, OA_REQ_FILE, OA_SYS_CFG_NAME
from extensions.octoapp.octoapp import Octoapp
from utils.common import check_install_dependencies, moonraker_exists
from utils.config_utils import remove_config_section
from utils.fs_utils import run_remove_routines
from utils.git_utils import git_clone_wrapper
from utils.input_utils import get_confirm
from utils.instance_utils import get_instances
from utils.sys_utils import install_python_requirements, parse_packages_from_file

class OctoappExtension(BaseExtension):

    def install_extension(self, **kwargs) -> None:
        Logger.print_status(translate('installing_octoapp_for_klipper_1edaec'))
        if not moonraker_exists():
            return
        force_clone = False
        OA_instances: List[Octoapp] = get_instances(Octoapp)
        if OA_instances:
            Logger.print_dialog(DialogType.INFO, [translate('octoapp_is_already_installed_6b9c3f'), 'It is safe to run the installer again to link your printer or repair any issues.'])
            if not get_confirm('Re-run OctoApp installation?'):
                Logger.print_info(translate('exiting_octoapp_for_klipper_installation_f8c742'))
                return
            else:
                Logger.print_status(translate('reinstalling_octoapp_for_klipper_4749ba'))
                force_clone = True
        mr_instances: List[Moonraker] = get_instances(Moonraker)
        mr_names = [f'● {moonraker.data_dir.name}' for moonraker in mr_instances]
        if len(mr_names) > 1:
            Logger.print_dialog(DialogType.INFO, [translate('the_following_moonraker_instances_were_603876'), *mr_names, '\n\n', 'The setup will apply the same names to OctoApp!'])
        if not get_confirm('Continue OctoApp for Klipper installation?', default_choice=True, allow_go_back=True):
            Logger.print_info(translate('exiting_octoapp_for_klipper_installation_f8c742'))
            return
        try:
            git_clone_wrapper(OA_REPO, OA_DIR, force=force_clone)
            for moonraker in mr_instances:
                instance = Octoapp(suffix=moonraker.suffix)
                instance.create()
            InstanceManager.restart_all(mr_instances)
            Logger.print_dialog(DialogType.SUCCESS, [translate('octoapp_for_klipper_successfully_installed_561471')], center_content=True)
        except Exception as e:
            Logger.print_error(f'Error during OctoApp for Klipper installation:\n{e}')

    def update_extension(self, **kwargs) -> None:
        Logger.print_status(translate('updating_octoapp_for_klipper_4aa852'))
        try:
            Octoapp.update()
            Logger.print_dialog(DialogType.SUCCESS, [translate('octoapp_for_klipper_successfully_updated_ea9abe')], center_content=True)
        except Exception as e:
            Logger.print_error(f'Error during OctoApp for Klipper update:\n{e}')

    def remove_extension(self, **kwargs) -> None:
        Logger.print_status(translate('removing_octoapp_for_klipper_c492d6'))
        mr_instances: List[Moonraker] = get_instances(Moonraker)
        ob_instances: List[Octoapp] = get_instances(Octoapp)
        try:
            self._remove_OA_instances(ob_instances)
            self._remove_OA_store_dirs()
            self._remove_OA_dir()
            self._remove_OA_env()
            remove_config_section(f'include {OA_SYS_CFG_NAME}', mr_instances)
            run_remove_routines(OA_INSTALLER_LOG_FILE)
            Logger.print_dialog(DialogType.SUCCESS, [translate('octoapp_for_klipper_successfully_removed_86bace')], center_content=True)
        except Exception as e:
            Logger.print_error(f'Error during OctoApp for Klipper removal:\n{e}')

    def _install_OA_dependencies(self) -> None:
        OA_deps = []
        if OA_DEPS_JSON_FILE.exists():
            with open(OA_DEPS_JSON_FILE, 'r') as deps:
                OA_deps = json.load(deps).get('debian', [])
        elif OA_INSTALL_SCRIPT.exists():
            OA_deps = parse_packages_from_file(OA_INSTALL_SCRIPT)
        if not OA_deps:
            raise ValueError(translate('error_reading_octoapp_dependencies_b9c8fd'))
        check_install_dependencies({*OA_deps})
        install_python_requirements(OA_ENV_DIR, OA_REQ_FILE)

    def _remove_OA_instances(self, instance_list: List[Octoapp]) -> None:
        if not instance_list:
            Logger.print_info(translate('no_octoapp_instances_found_skipped_ecf17a'))
            return
        for instance in instance_list:
            Logger.print_status(f'Removing instance {instance.service_file_path.stem} ...')
            InstanceManager.remove(instance)

    def _remove_OA_dir(self) -> None:
        Logger.print_status(translate('removing_octoapp_for_klipper_directory_76a873'))
        if not OA_DIR.exists():
            Logger.print_info(f"'{OA_DIR}' does not exist. Skipped ...")
            return
        run_remove_routines(OA_DIR)

    def _remove_OA_store_dirs(self) -> None:
        Logger.print_status(translate('removing_octoapp_for_klipper_store_2571de'))
        klipper_instances: List[Moonraker] = get_instances(Klipper)
        for instance in klipper_instances:
            store_dir = instance.data_dir.joinpath('octoapp-store')
            if not store_dir.exists():
                Logger.print_info(f"'{store_dir}' does not exist. Skipped ...")
                return
            run_remove_routines(store_dir)

    def _remove_OA_env(self) -> None:
        Logger.print_status(translate('removing_octoapp_for_klipper_environment_0f915d'))
        if not OA_ENV_DIR.exists():
            Logger.print_info(f"'{OA_ENV_DIR}' does not exist. Skipped ...")
            return
        run_remove_routines(OA_ENV_DIR)