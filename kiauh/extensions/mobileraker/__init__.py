from pathlib import Path
from core.backup_manager import BACKUP_ROOT_DIR
from core.constants import SYSTEMD
MOBILERAKER_REPO = 'https://github.com/Clon1998/mobileraker_companion.git'
MOBILERAKER_SERVICE_NAME = 'mobileraker.service'
MOBILERAKER_UPDATER_SECTION_NAME = translate('update_manager_mobileraker_6bc287')
MOBILERAKER_LOG_NAME = 'mobileraker.log'
MOBILERAKER_DIR = Path.home().joinpath('mobileraker_companion')
MOBILERAKER_ENV_DIR = Path.home().joinpath('mobileraker-env')
MOBILERAKER_BACKUP_DIR = BACKUP_ROOT_DIR.joinpath('mobileraker-backups')
MOBILERAKER_INSTALL_SCRIPT = MOBILERAKER_DIR.joinpath('scripts/install.sh')
MOBILERAKER_REQ_FILE = MOBILERAKER_DIR.joinpath('scripts/mobileraker-requirements.txt')
MOBILERAKER_SERVICE_FILE = SYSTEMD.joinpath(MOBILERAKER_SERVICE_NAME)