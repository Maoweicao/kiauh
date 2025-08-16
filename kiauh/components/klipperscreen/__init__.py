from pathlib import Path
from core.backup_manager import BACKUP_ROOT_DIR
from core.constants import SYSTEMD
KLIPPERSCREEN_REPO = 'https://github.com/KlipperScreen/KlipperScreen.git'
KLIPPERSCREEN_SERVICE_NAME = 'KlipperScreen.service'
KLIPPERSCREEN_UPDATER_SECTION_NAME = translate('update_manager_klipperscreen_5000b5')
KLIPPERSCREEN_LOG_NAME = 'KlipperScreen.log'
KLIPPERSCREEN_DIR = Path.home().joinpath('KlipperScreen')
KLIPPERSCREEN_ENV_DIR = Path.home().joinpath('.KlipperScreen-env')
KLIPPERSCREEN_BACKUP_DIR = BACKUP_ROOT_DIR.joinpath('klipperscreen-backups')
KLIPPERSCREEN_REQ_FILE = KLIPPERSCREEN_DIR.joinpath('scripts/KlipperScreen-requirements.txt')
KLIPPERSCREEN_INSTALL_SCRIPT = KLIPPERSCREEN_DIR.joinpath('scripts/KlipperScreen-install.sh')
KLIPPERSCREEN_SERVICE_FILE = SYSTEMD.joinpath(KLIPPERSCREEN_SERVICE_NAME)