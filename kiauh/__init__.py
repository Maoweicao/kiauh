# ======================================================================= #
#  Copyright (C) 2020 - 2025 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #

import sys
from pathlib import Path
import builtins

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APPLICATION_ROOT = Path(__file__).resolve().parent
sys.path.append(str(APPLICATION_ROOT))

# Provide a package-level i18n helper and expose a global translate()
try:
	# import lazily from our new i18n module
	from .i18n import translate, set_locale, TRANSLATIONS  # type: ignore
	__all__ = ['translate', 'set_locale', 'TRANSLATIONS']
	# Inject into builtins so modules that call translate() without importing it keep working
	if not hasattr(builtins, 'translate'):
		builtins.translate = translate
except Exception:
	# Best-effort: if import fails (e.g., during early install), skip injection
	pass
