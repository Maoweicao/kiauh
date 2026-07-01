# ======================================================================= #
#  Copyright (C) 2020 - 2026 Dominik Willner <th33xitus@gmail.com>        #
#                                                                         #
#  This file is part of KIAUH - Klipper Installation And Update Helper    #
#  https://github.com/dw-0/kiauh                                          #
#                                                                         #
#  This file may be distributed under the terms of the GNU GPLv3 license  #
# ======================================================================= #

from pathlib import Path

# Service names for systemd status checking
KLIPPER_SERVICE = "klipper"
MOONRAKER_SERVICE = "moonraker"
NGINX_SERVICE = "nginx"

# Client directories used to detect Mainsail/Fluidd installation
MAINSAIL_DIR = Path.home().joinpath("mainsail")
FLUIDD_DIR = Path.home().joinpath("fluidd")

# NGINX config paths
NGINX_SITES_ENABLED = Path("/etc/nginx/sites-enabled")
