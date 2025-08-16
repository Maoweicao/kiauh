# KIAUH 国际化审计报告

生成时间: 2025-08-16 20:35:19

总结:

- 硬编码可能需要国际化的文本: 726
- translate() 调用次数: 6
- TRANSLATIONS 查找次数: 1

## 按文件详情

### kiauh\components\crowsnest\crowsnest.py

**硬编码字符串示例**:

- L63 (Logger.print): `Crowsnest installation aborted!`
- L63 (constant): `Crowsnest installation aborted!`
- L66 (Logger.print): `Launching crowsnest's install configurator ...`
- L71 (Logger.print): `Launching crowsnest installer ...`
- L72 (Logger.print): `Installer will prompt you for sudo password!`
- L89 (constant): `Multi instance install detected!`
- L95 (constant): `The following instances were found:`
- L116 (Logger.print): `Generating .config failed, installation aborted`
- L126 (Logger.print): `Updating Crowsnest ...`
- L144 (Logger.print): `Crowsnest updated successfully.`
- L161 (Logger.print): `Crowsnest does not seem to be installed! Skipping ...`
- L166 (constant): `make uninstall`
- L175 (Logger.print): `Removing crowsnest directory ...`
- L177 (Logger.print): `Directory removed!`
- L177 (constant): `Directory removed!`

### kiauh\components\klipper\klipper.py

**硬编码字符串示例**:

- L62 (Logger.print): `Creating new Klipper Instance ...`
- L78 (constant): `Error creating instance: `
- L81 (constant): `Error creating env file: `
- L91 (constant): `Unable to open `
- L91 (constant): ` - File not found`
- L119 (constant): `Unable to open `
- L119 (constant): ` - File not found`

### kiauh\components\klipper\klipper_dialogs.py

**硬编码字符串示例**:

- L40 (constant): ` were found:`
- L65 (constant): `WARNING:`
- L87 (constant): `INFO:`

### kiauh\components\klipper\klipper_utils.py

**硬编码字符串示例**:

- L74 (constant): ` Klipper instances to set up`
- L88 (constant): `Enter name for instance `
- L110 (constant): `INFO:`
- L127 (constant): `Unable to add user to usergroups: `
- L160 (constant): `KIAUH was unable to mask the `
- L222 (Logger.print): `Required Klipper python environment not found!`
- L239 (constant): `Install Input Shaper Dependencies`
- L76 (fstring): `Klipper instances to set up`

### kiauh\components\klipper\menus\klipper_remove_menu.py

**硬编码字符串示例**:

- L25 (constant): `Remove Klipper`

### kiauh\components\klipper\services\klipper_setup_service.py

**硬编码字符串示例**:

- L107 (Logger.print): `Installing Klipper ...`
- L145 (Logger.print): `Klipper installation failed!`
- L145 (constant): `Klipper installation failed!`
- L186 (Logger.print): `Removing Klipper instances ...`
- L194 (constant): `● Klipper instances removed: `
- L197 (Logger.print): `No Klipper Services installed! Skipped ...`
- L207 (Logger.print): `Removing Klipper local repository ...`
- L209 (constant): `● Klipper local repository removed`
- L211 (Logger.print): `Removing Klipper Python environment ...`
- L283 (Logger.print): `Error during installation of Klipper requirements!`
- L283 (constant): `Error during installation of Klipper requirements!`
- L294 (constant): `The following Klipper instances will be installed:`
- L335 (constant): `Select Klipper instance to remove`
- L361 (constant): `Remove '`
- L361 (fstring): `Remove`

### kiauh\components\klipper_firmware\firmware_utils.py

**硬编码字符串示例**:

- L58 (Logger.print): `Unable to find a USB device!`
- L58 (constant): `Unable to find a USB device!`
- L74 (Logger.print): `Unable to find a UART device!`
- L74 (constant): `Unable to find a UART device!`
- L89 (Logger.print): `Unable to find a USB DFU device!`
- L89 (constant): `Unable to find a USB DFU device!`
- L104 (Logger.print): `Unable to find a USB RP2 Boot device!`
- L104 (constant): `Unable to find a USB RP2 Boot device!`
- L118 (constant): `An unexpected error occured:
`
- L148 (constant): `Unable to find Klippers sdcard flash script!`
- L168 (constant): `Flashing failed with returncode: `
- L170 (Logger.print): `Flashing successful!`
- L170 (constant): `Flashing successful!`
- L173 (Logger.print): `Flashing failed!`
- L173 (constant): `Flashing failed!`
- L174 (Logger.print): `See the console output above!`
- L186 (constant): `Unexpected error:
`
- L199 (constant): `Unexpected error:
`
- L212 (constant): `Unexpected error:
`

### kiauh\components\klipper_firmware\menus\klipper_build_menu.py

**硬编码字符串示例**:

- L150 (constant): `Press ENTER to install dependencies`
- L188 (Logger.print): `Installing system packages...`
- L192 (Logger.print): `Installing dependencies failed!`
- L192 (constant): `Installing dependencies failed!`
- L203 (Logger.print): `Firmware successfully built!`
- L203 (constant): `Firmware successfully built!`
- L211 (Logger.print): `Building Klipper Firmware failed!`
- L211 (constant): `Building Klipper Firmware failed!`
- L265 (Logger.print): `Aborted saving firmware config ...`
- L204 (fstring): `Firmware file located in`

### kiauh\components\klipper_firmware\menus\klipper_flash_error_menu.py

**硬编码字符串示例**:

- L25 (constant): `!!! NO FIRMWARE FILE FOUND !!!`
- L72 (constant): `!!! ERROR GETTING BOARD LIST !!!`
- L86 (constant): `Reading the list of supported boards failed!`

### kiauh\components\klipper_firmware\menus\klipper_flash_help_menu.py

**硬编码字符串示例**:

- L43 (constant): `Updating via SD-Card Update:`

### kiauh\components\klipper_firmware\menus\klipper_flash_menu.py

**硬编码字符串示例**:

- L170 (constant): `Select connection type`
- L222 (Logger.print): `Identifying MCU connected via USB ...`
- L225 (Logger.print): `Identifying MCU possibly connected via UART ...`
- L228 (Logger.print): `Identifying MCU connected via USB in DFU mode ...`
- L231 (Logger.print): `Identifying MCU connected via USB in RP2 Boot mode ...`
- L237 (Logger.print): `No MCUs found!`
- L237 (constant): `No MCUs found!`
- L238 (Logger.print): `Make sure they are connected and repeat this step.`
- L242 (Logger.print): `The following MCUs were found:`
- L242 (constant): `The following MCUs were found:`
- L280 (constant): `List of detected MCUs`
- L320 (Logger.print): `Flashing failed!`
- L320 (constant): `Flashing failed!`
- L374 (Logger.print): `Board selection failed!`
- L374 (constant): `Board selection failed!`
- L387 (constant): `Please set the baud rate`
- L477 (Logger.print): `Returning to MCU Flash Menu in 5 seconds ...`

### kiauh\components\klipperscreen\__init__.py

**硬编码字符串示例**:

- L19 (constant): `update_manager KlipperScreen`

### kiauh\components\klipperscreen\klipperscreen.py

**硬编码字符串示例**:

- L55 (Logger.print): `Installing KlipperScreen ...`
- L89 (Logger.print): `Moonraker is not installed! Cannot add KlipperScreen to update manager!`
- L90 (constant): `Moonraker is not installed! Cannot add KlipperScreen to update manager!`
- L93 (Logger.print): `KlipperScreen successfully installed!`
- L93 (constant): `KlipperScreen successfully installed!`
- L95 (constant): `Error installing KlipperScreen:
`
- L110 (constant): `install_script`
- L117 (Logger.print): `KlipperScreen does not seem to be installed! Skipping ...`
- L121 (Logger.print): `Updating KlipperScreen ...`
- L135 (Logger.print): `KlipperScreen updated successfully.`
- L137 (constant): `Error updating KlipperScreen:
`
- L150 (Logger.print): `Removing KlipperScreen ...`
- L153 (Logger.print): `Removing KlipperScreen directory ...`
- L155 (Logger.print): `KlipperScreen directory successfully removed!`
- L155 (constant): `KlipperScreen directory successfully removed!`
- L157 (Logger.print): `KlipperScreen directory not found!`
- L157 (constant): `KlipperScreen directory not found!`
- L160 (Logger.print): `Removing KlipperScreen environment ...`
- L162 (Logger.print): `KlipperScreen environment successfully removed!`
- L162 (constant): `KlipperScreen environment successfully removed!`
- L164 (Logger.print): `KlipperScreen environment not found!`
- L164 (constant): `KlipperScreen environment not found!`
- L171 (Logger.print): `Removing KlipperScreen log file ...`
- L173 (Logger.print): `KlipperScreen log file successfully removed!`
- L173 (constant): `KlipperScreen log file successfully removed!`
- L181 (constant): ` successfully removed!`
- L185 (Logger.print): `Removing KlipperScreen from update manager ...`
- L186 (constant): `update_manager KlipperScreen`
- L187 (Logger.print): `KlipperScreen successfully removed from update manager!`
- L187 (constant): `KlipperScreen successfully removed from update manager!`
- L189 (Logger.print): `KlipperScreen successfully removed!`
- L189 (constant): `KlipperScreen successfully removed!`
- L192 (constant): `Error removing KlipperScreen:
`

### kiauh\components\log_uploads\log_upload_utils.py

**硬编码字符串示例**:

- L43 (constant): `Uploading the following logfile from `
- L51 (Logger.print): `Upload successful! Access it via the following link:`
- L51 (constant): `Upload successful! Access it via the following link:`
- L54 (Logger.print): `Uploading logfile failed!`
- L54 (constant): `Uploading logfile failed!`

### kiauh\components\log_uploads\menus\log_upload_menu.py

**硬编码字符串示例**:

- L67 (Logger.print): `Log upload failed!`
- L67 (constant): `Log upload failed!`

### kiauh\components\moonraker\menus\moonraker_remove_menu.py

**硬编码字符串示例**:

- L25 (constant): `Remove Moonraker`

### kiauh\components\moonraker\moonraker.py

**硬编码字符串示例**:

- L68 (Logger.print): `Creating new Moonraker Instance ...`
- L83 (constant): `Error creating instance: `
- L86 (constant): `Error creating env file: `
- L96 (constant): `Unable to open `
- L96 (constant): ` - File not found`
- L124 (constant): `Unable to open `
- L124 (constant): ` - File not found`

### kiauh\components\moonraker\moonraker_dialogs.py

**硬编码字符串示例**:

- L25 (constant): `The following instances were found:`
- L54 (constant): `PLEASE NOTE:`
- L56 (constant): `If you select an instance with an existing Moonraker`

### kiauh\components\moonraker\services\moonraker_setup_service.py

**硬编码字符串示例**:

- L138 (constant): `Select Klipper instance to setup Moonraker for`
- L153 (constant): `Error selecting instance!`
- L162 (constant): `Error while installing Moonraker: `
- L204 (Logger.print): `Removing Moonraker instances ...`
- L212 (constant): `● Moonraker instances removed: `
- L215 (Logger.print): `No Moonraker Services installed! Skipped ...`
- L228 (Logger.print): `Removing all Moonraker policykit rules ...`
- L230 (constant): `● Moonraker policykit rules removed`
- L232 (Logger.print): `Removing Moonraker local repository ...`
- L234 (constant): `● Moonraker local repository removed`
- L236 (Logger.print): `Removing Moonraker Python environment ...`
- L294 (constant): `Moonraker successfully installed!`
- L302 (Logger.print): `Klipper not installed!`
- L302 (constant): `Klipper not installed!`
- L303 (Logger.print): `Moonraker cannot be installed! Install Klipper first.`
- L326 (Logger.print): `Error during installation of Moonraker requirements!`
- L326 (constant): `Error during installation of Moonraker requirements!`
- L330 (Logger.print): `Installing Moonraker policykit rules ...`
- L337 (Logger.print): `Moonraker policykit rules are already installed.`
- L350 (Logger.print): `Installing Moonraker policykit rules failed!`
- L350 (constant): `Installing Moonraker policykit rules failed!`
- L353 (Logger.print): `Moonraker policykit rules successfully installed!`
- L353 (constant): `Moonraker policykit rules successfully installed!`
- L356 (constant): `Error while installing Moonraker policykit rules: `
- L377 (constant): `Select Moonraker instance to remove`
- L403 (constant): `Remove '`
- L403 (fstring): `Remove`

### kiauh\components\moonraker\utils\sysdeps_parser.py

**硬编码字符串示例**:

- L92 (constant): `Invalid logical operator `
- L150 (constant): `Failed to detect current distro ID, cannot parse dependencies`
- L75 (fstring): `Requirement specifier is missing an expression`
- L100 (fstring): `Requirement specifier contains two seqential expressions`
- L158 (fstring): `Dependency data contains an empty package definition`
- L170 (fstring): `Dependency data has no package definition for linux`

### kiauh\components\moonraker\utils\utils.py

**硬编码字符串示例**:

- L47 (Logger.print): `Parsing Moonraker system dependencies  ...`
- L52 (constant): `Parsing system dependencies from `
- L59 (constant): ` not found!`
- L61 (constant): `Parsing system dependencies from `
- L66 (constant): `Error parsing Moonraker dependencies!`
- L82 (constant): `Error while removing policykit rules: `
- L140 (constant): `update_manager `
- L154 (constant): `update_manager `
- L193 (constant): `Unable to parse `

### kiauh\components\webui_client\base_data.py

**硬编码字符串示例**:

- L30 (constant): `Base class for webclient data`

### kiauh\components\webui_client\client_config\client_config_remove.py

**硬编码字符串示例**:

- L36 (constant): ` removed`
- L63 (constant): ` removed from instance`
- L72 (constant): `' removed for instance`
- L79 (constant): `update_manager `
- L81 (constant): `' removed for instance`

### kiauh\components\webui_client\client_config\client_config_setup.py

**硬编码字符串示例**:

- L42 (Logger.print): `Another Client-Config is already installed! Skipped ...`
- L47 (constant): `Re-install `
- L63 (constant): `update_manager `
- L77 (constant): ` installation failed!
`
- L90 (constant): ` failed!`
- L101 (constant): `Unable to update `
- L111 (constant): `Successfully updated `
- L112 (Logger.print): `Restart Klipper to reload the configuration!`
- L126 (Logger.print): `Creating symlink failed!`
- L126 (constant): `Creating symlink failed!`

### kiauh\components\webui_client\client_dialogs.py

**硬编码字符串示例**:

- L20 (constant): `No local Moonraker installation was found!`
- L22 (constant): `It is possible to install `
- L34 (constant): ` seems to be already installed!`
- L44 (constant): `Please select the port, `
- L56 (constant): `The following ports were found to be already in use:`

### kiauh\components\webui_client\client_remove.py

**硬编码字符串示例**:

- L53 (constant): ` removed`
- L57 (constant): `● NGINX logs removed`
- L59 (constant): `update_manager `
- L66 (constant): `' removed for instance: `
- L104 (constant): `Removing NGINX logs for `

### kiauh\components\webui_client\client_setup.py

**硬编码字符串示例**:

- L102 (constant): `update_manager `
- L137 (constant): ` installation failed!`
- L161 (Logger.print): `Download complete!`
- L166 (Logger.print): `OK!`
- L169 (constant): ` failed!`
- L177 (constant): `Unable to update `
- L183 (constant): `Creating temporary backup of `

### kiauh\components\webui_client\client_utils.py

**硬编码字符串示例**:

- L117 (Logger.print): `Enable Mainsails remote mode ...`
- L123 (Logger.print): `Remote mode already configured. Skipped ...`
- L126 (Logger.print): `Setting instance storage location to 'browser' ...`
- L131 (Logger.print): `Mainsails remote mode enabled!`
- L137 (Logger.print): `Link NGINX logs into log directory ...`
- L310 (constant): `Unable to create '`
- L335 (constant): ` failed!`
- L374 (constant): `Unable to parse listen port `
- L426 (Logger.print): `This port is already in use. Please select another one.`
- L310 (fstring): `Unable to create`

### kiauh\components\webui_client\menus\client_install_menu.py

**硬编码字符串示例**:

- L36 (constant): `Installation Menu > `
- L81 (Logger.print): `Saving new port configuration ...`
- L84 (Logger.print): `Port configuration saved!`

### kiauh\components\webui_client\menus\client_remove_menu.py

**硬编码字符串示例**:

- L27 (constant): `Remove `
- L62 (constant): ` Remove `
- L62 (constant): ` Remove `

### kiauh\core\backup_manager\backup_manager.py

**硬编码字符串示例**:

- L53 (Logger.print): `File does not exist! Skipping ...`
- L66 (Logger.print): `Backup successful!`
- L66 (constant): `Backup successful!`
- L69 (constant): `Unable to backup '`
- L81 (Logger.print): `Source directory does not exist! Skipping ...`
- L95 (Logger.print): `Backup successful!`
- L95 (constant): `Backup successful!`
- L100 (constant): `Unable to backup directory '`
- L101 (constant): `Unable to backup directory '`
- L69 (fstring): `Unable to backup`
- L100 (fstring): `Unable to backup directory`
- L101 (fstring): `Unable to backup directory`

### kiauh\core\instance_manager\instance_manager.py

**硬编码字符串示例**:

- L36 (constant): `Error disabling `
- L45 (constant): `Error starting `
- L54 (constant): `Error stopping `
- L63 (constant): `Error restarting `
- L103 (constant): `Remove '`
- L103 (fstring): `Remove`

### kiauh\core\logger.py

**硬编码字符串示例**:

- L19 (constant): `INFO`
- L20 (constant): `SUCCESS`
- L22 (constant): `WARNING`
- L23 (constant): `ERROR`
- L44 (constant): `Success!`

### kiauh\core\menus\base_menu.py

**硬编码字符串示例**:

- L34 (constant): `Klipper Installation And Update Helper`
- L92 (print): `╚═══════════════════════════════════════════════════════╝`
- L160 (Logger.print): `###### Happy printing!`
- L238 (constant): `An unexpected error occured:
`

### kiauh\core\menus\install_menu.py

**硬编码字符串示例**:

- L36 (constant): `Installation Menu`

### kiauh\core\menus\main_menu.py

**硬编码字符串示例**:

- L60 (constant): `MainMenu does not have a previous menu`
- L81 (constant): `Not installed`
- L154 (Logger.print): `###### Happy printing!`

### kiauh\core\menus\remove_menu.py

**硬编码字符串示例**:

- L33 (constant): `Remove Menu`

### kiauh\core\menus\repo_select_menu.py

**硬编码字符串示例**:

- L37 (constant): `Klipper Repository Selection Menu`
- L40 (constant): `Moonraker Repository Selection Menu`

### kiauh\core\menus\settings_menu.py

**硬编码字符串示例**:

- L185 (Logger.print): `Invalid selection`
- L187 (Logger.print): `Invalid input`

### kiauh\core\menus\update_menu.py

**硬编码字符串示例**:

- L53 (constant): `Loading update menu, please wait`
- L56 (constant): `Update Menu`
- L77 (constant): `installed`
- L83 (constant): `installed`
- L89 (constant): `installed`
- L95 (constant): `installed`
- L101 (constant): `installed`
- L107 (constant): `installed`
- L113 (constant): `installed`
- L119 (constant): `installed`
- L184 (Logger.print): `Updating all components ...`
- L272 (constant): `installed`
- L290 (constant): `installed`
- L311 (Logger.print): `No system upgrades available!`
- L319 (constant): `UPGRADABLE SYSTEM UPDATES`
- L323 (Logger.print): `Upgrading system packages ...`
- L326 (constant): `Error upgrading system packages:
`

### kiauh\core\settings\kiauh_settings.py

**硬编码字符串示例**:

- L34 (constant): `Raised when a value is invalid for an option`
- L157 (constant): `backup_before_update`
- L305 (constant): `backup_before_update`
- L420 (constant): `Successfully migrated `
- L427 (Logger.print): `Please migrate manually.`

### kiauh\core\submodules\simple_config_parser\src\simple_config_parser\simple_config_parser.py

**硬编码字符串示例**:

- L28 (constant): `Raised when a section is not defined`
- L36 (constant): `Raised when a section is defined more than once`
- L44 (constant): `Raised when an option is not defined in a section`
- L51 (constant): `Raised when a line is not recognized as any known type`
- L70 (constant): `Wheter or not the given line matches the definition of a section`
- L74 (constant): `Wheter or not the given line matches the definition of an option`
- L78 (constant): `Wheter or not the given line matches the definition of a multiline option`
- L86 (constant): `Wheter or not the given line matches the definition of an empty line`
- L90 (constant): `Parses a line and determines its type`
- L150 (constant): `File path cannot be None`
- L198 (constant): `Check if a section exists`
- L215 (constant): `Check if there is a blank line between the last section and the new section`
- L249 (constant): `Return a list of all option names for a given section`
- L258 (constant): `Check if an option exists in a section`
- L309 (constant): `Remove an option from a section`
- L364 (constant): `Return the value of the given option in the given section as an int`
- L370 (constant): `Return the value of the given option in the given section as a float`
- L376 (constant): `Return the value of the given option in the given section as a boolean`
- L382 (constant): `Convert a string to a boolean`
- L396 (constant): `Return the value of the given option in the given section as a converted value`

### kiauh\core\types\component_status.py

**硬编码字符串示例**:

- L14 (constant): `Installed`
- L14 (constant): `Not installed`
- L17 (constant): `Not installed`
- L19 (constant): `Installed`

### kiauh\extensions\extensions_menu.py

**硬编码字符串示例**:

- L79 (constant): `Failed loading extension `
- L102 (print): `╟───────────────────────────────────────────────────────╢`
- L124 (constant): `updates`
- L153 (constant): `updates`

### kiauh\extensions\gcode_shell_cmd\gcode_shell_cmd_extension.py

**硬编码字符串示例**:

- L41 (Logger.print): `No Klipper directory found! Unable to install extension.`
- L56 (Logger.print): `Installation aborted due to user request.`
- L66 (constant): `Unable to install extension: `
- L74 (Logger.print): `Installing G-Code Shell Command extension successful!`
- L79 (Logger.print): `Extension does not seem to be installed! Skipping ...`
- L87 (Logger.print): `Extension successfully removed!`
- L87 (constant): `Extension successfully removed!`
- L89 (constant): `Unable to remove extension: `
- L91 (Logger.print): `PLEASE NOTE:`
- L91 (constant): `PLEASE NOTE:`
- L92 (Logger.print): `Remaining gcode shell command will cause Klipper to throw an error.`
- L95 (Logger.print): `Make sure to remove them from the printer.cfg!`
- L103 (Logger.print): `File already exists! Skipping ...`
- L107 (Logger.print): `Done!`
- L127 (Logger.print): `Section already defined! Skipping ...`
- L131 (Logger.print): `Done!`

### kiauh\extensions\klipper_backup\klipper_backup_extension.py

**硬编码字符串示例**:

- L34 (Logger.print): `Extension does not seem to be installed! Skipping ...`
- L46 (constant): ` successfully removed!`
- L48 (constant): `reset-failed`
- L54 (constant): `Failed to remove `
- L68 (constant): `install-files`
- L81 (Logger.print): `Removing Klipper-Backup moonraker entry ...`
- L90 (Logger.print): `Klipper-Backup moonraker entry successfully removed!`
- L90 (constant): `Klipper-Backup moonraker entry successfully removed!`
- L111 (Logger.print): `Removing Klipper-Backup crontab entry ...`
- L126 (Logger.print): `Klipper-Backup crontab entry successfully removed!`
- L127 (constant): `Klipper-Backup crontab entry successfully removed!`
- L130 (Logger.print): `Unable to remove the Klipper-Backup cron entry`
- L130 (constant): `Unable to remove the Klipper-Backup cron entry`
- L136 (Logger.print): `Unable to remove the Klipper-Backup moonraker entry`
- L137 (constant): `Unable to remove the Klipper-Backup moonraker entry`
- L141 (Logger.print): `Removing Klipper-Backup extension ...`
- L146 (Logger.print): `Extension Klipper-Backup successfully removed!`
- L146 (constant): `Extension Klipper-Backup successfully removed!`
- L148 (Logger.print): `Unable to remove Klipper-Backup extension`
- L148 (constant): `Unable to remove Klipper-Backup extension`
- L158 (Logger.print): `Extension does not seem to be installed! Skipping ...`
- L160 (constant): `check_updates`

### kiauh\extensions\mainsail_theme_installer\mainsail_theme_installer_extension.py

**硬编码字符串示例**:

- L62 (constant): `Uninstalling theme from `
- L69 (Logger.print): `Theme successfully uninstalled!`
- L69 (constant): `Theme successfully uninstalled!`
- L71 (Logger.print): `Unable to uninstall theme`
- L71 (constant): `Unable to uninstall theme`
- L83 (constant): `Mainsail Theme Installer`
- L103 (constant): `A preview of each Mainsail theme can be found here:`
- L139 (constant): `No option index provided`
- L163 (Logger.print): `Info from the creator:`
- L163 (constant): `Info from the creator:`
- L174 (constant): `Select the printer to install the theme for`
- L176 (constant): `Select the printer to remove the theme from`

### kiauh\extensions\mobileraker\__init__.py

**硬编码字符串示例**:

- L20 (constant): `update_manager mobileraker`

### kiauh\extensions\mobileraker\mobileraker_extension.py

**硬编码字符串示例**:

- L49 (Logger.print): `Installing Mobileraker's companion ...`
- L82 (Logger.print): `Moonraker is not installed! Cannot add Mobileraker's companion to update manager!`
- L86 (Logger.print): `Mobileraker's companion successfully installed!`
- L94 (Logger.print): `Mobileraker's companion doesn't seem to be installed! Skipping ...`
- L99 (Logger.print): `Updating Mobileraker's companion ...`
- L113 (Logger.print): `Mobileraker's companion updated successfully.`
- L119 (Logger.print): `Removing Mobileraker's companion ...`
- L122 (Logger.print): `Removing Mobileraker's companion directory ...`
- L124 (Logger.print): `Mobileraker's companion directory successfully removed!`
- L128 (Logger.print): `Mobileraker's companion directory not found!`
- L131 (Logger.print): `Removing Mobileraker's companion environment ...`
- L133 (Logger.print): `Mobileraker's companion environment successfully removed!`
- L137 (Logger.print): `Mobileraker's companion environment not found!`
- L148 (constant): ` successfully removed!`
- L152 (Logger.print): `Removing Mobileraker's companion from update manager ...`
- L156 (Logger.print): `Mobileraker's companion successfully removed from update manager!`
- L160 (Logger.print): `Mobileraker's companion successfully removed!`
- L177 (constant): `install_script`
- L88 (fstring): `Error installing Mobileraker`
- L115 (fstring): `Error updating Mobileraker`
- L163 (fstring): `Error removing Mobileraker`

### kiauh\extensions\obico\moonraker_obico.py

**硬编码字符串示例**:

- L63 (Logger.print): `Creating new Obico for Klipper Instance ...`
- L77 (constant): `Error creating instance: `
- L80 (constant): `Error creating env file: `
- L85 (constant): `Linking instance for printer `
- L93 (constant): `Error during Obico linking: `
- L103 (constant): `Unable to open `
- L103 (constant): ` - File not found`
- L131 (constant): `Unable to open `
- L131 (constant): ` - File not found`

### kiauh\extensions\obico\moonraker_obico_extension.py

**硬编码字符串示例**:

- L57 (Logger.print): `Installing Obico for Klipper ...`
- L72 (Logger.print): `Exiting Obico for Klipper installation ...`
- L81 (Logger.print): `Re-Installing Obico for Klipper ...`
- L135 (constant): `Obico for Klipper successfully installed!`
- L140 (constant): `Error during Obico for Klipper installation:
`
- L143 (Logger.print): `Updating Obico for Klipper ...`
- L152 (Logger.print): `Obico for Klipper successfully updated!`
- L152 (constant): `Obico for Klipper successfully updated!`
- L155 (constant): `Error during Obico for Klipper update:
`
- L158 (Logger.print): `Removing Obico for Klipper ...`
- L172 (constant): `Obico for Klipper successfully removed!`
- L177 (constant): `Error during Obico for Klipper removal:
`
- L203 (constant): `The following Moonraker instances were found:`
- L214 (constant): `Obico is already installed!`
- L310 (Logger.print): `Checking link status of Obico instances ...`
- L330 (constant): `For more information visit:`
- L338 (Logger.print): `Linking to Obico server skipped ...`
- L348 (Logger.print): `No Obico instances found. Skipped ...`
- L358 (Logger.print): `Removing Obico for Klipper directory ...`
- L367 (Logger.print): `Removing Obico for Klipper environment ...`

### kiauh\extensions\octoapp\octoapp.py

**硬编码字符串示例**:

- L56 (Logger.print): `Creating OctoApp for Klipper Instance ...`
- L63 (constant): `Error creating instance: `
- L72 (constant): `Error updating OctoApp for Klipper: `

### kiauh\extensions\octoapp\octoapp_extension.py

**硬编码字符串示例**:

- L48 (Logger.print): `Installing OctoApp for Klipper ...`
- L60 (constant): `OctoApp is already installed!`
- L66 (Logger.print): `Exiting OctoApp for Klipper installation ...`
- L69 (Logger.print): `Re-Installing OctoApp for Klipper ...`
- L79 (constant): `The following Moonraker instances were found:`
- L91 (Logger.print): `Exiting OctoApp for Klipper installation ...`
- L105 (constant): `OctoApp for Klipper successfully installed!`
- L110 (constant): `Error during OctoApp for Klipper installation:
`
- L113 (Logger.print): `Updating OctoApp for Klipper ...`
- L118 (constant): `OctoApp for Klipper successfully updated!`
- L123 (constant): `Error during OctoApp for Klipper update:
`
- L126 (Logger.print): `Removing OctoApp for Klipper ...`
- L140 (constant): `OctoApp for Klipper successfully removed!`
- L145 (constant): `Error during OctoApp for Klipper removal:
`
- L156 (constant): `Error reading OctoApp dependencies!`
- L166 (Logger.print): `No OctoApp instances found. Skipped ...`
- L176 (Logger.print): `Removing OctoApp for Klipper directory ...`
- L185 (Logger.print): `Removing OctoApp for Klipper store directory ...`
- L198 (Logger.print): `Removing OctoApp for Klipper environment ...`

### kiauh\extensions\octoeverywhere\octoeverywhere.py

**硬编码字符串示例**:

- L58 (Logger.print): `Creating OctoEverywhere for Klipper Instance ...`
- L65 (constant): `Error creating instance: `
- L74 (constant): `Error updating OctoEverywhere for Klipper: `

### kiauh\extensions\octoeverywhere\octoeverywhere_extension.py

**硬编码字符串示例**:

- L47 (Logger.print): `Installing OctoEverywhere for Klipper ...`
- L59 (constant): `OctoEverywhere is already installed!`
- L65 (Logger.print): `Exiting OctoEverywhere for Klipper installation ...`
- L68 (Logger.print): `Re-Installing OctoEverywhere for Klipper ...`
- L78 (constant): `The following Moonraker instances were found:`
- L90 (Logger.print): `Exiting OctoEverywhere for Klipper installation ...`
- L104 (constant): `OctoEverywhere for Klipper successfully installed!`
- L110 (constant): `Error during OctoEverywhere for Klipper installation:
`
- L114 (Logger.print): `Updating OctoEverywhere for Klipper ...`
- L119 (constant): `OctoEverywhere for Klipper successfully updated!`
- L124 (constant): `Error during OctoEverywhere for Klipper update:
`
- L127 (Logger.print): `Removing OctoEverywhere for Klipper ...`
- L140 (constant): `OctoEverywhere for Klipper successfully removed!`
- L145 (constant): `Error during OctoEverywhere for Klipper removal:
`
- L156 (constant): `Error reading OctoEverywhere dependencies!`
- L166 (Logger.print): `No OctoEverywhere instances found. Skipped ...`
- L176 (Logger.print): `Removing OctoEverywhere for Klipper directory ...`
- L185 (Logger.print): `Removing OctoEverywhere for Klipper environment ...`

### kiauh\extensions\pretty_gcode\pretty_gcode_extension.py

**硬编码字符串示例**:

- L33 (Logger.print): `Installing PrettyGCode for Klipper ...`
- L45 (constant): `On which port should PrettyGCode run`
- L60 (constant): `PrettyGCode for Klipper`
- L70 (Logger.print): `PrettyGCode installation complete!`
- L75 (constant): `Error during PrettyGCode for Klipper installation: `
- L79 (Logger.print): `Updating PrettyGCode for Klipper ...`
- L84 (constant): `Error during PrettyGCode for Klipper update: `
- L88 (Logger.print): `Removing PrettyGCode for Klipper ...`
- L98 (Logger.print): `PrettyGCode for Klipper removed!`
- L98 (constant): `PrettyGCode for Klipper removed!`
- L101 (constant): `Error during PrettyGCode for Klipper removal: `

### kiauh\extensions\simply_print\simply_print_extension.py

**硬编码字符串示例**:

- L25 (Logger.print): `Installing SimplyPrint ...`
- L27 (constant): `SimplyPrint Installer`
- L40 (Logger.print): `Exiting SimplyPrint installation ...`
- L47 (constant): `Error during SimplyPrint installation:
`
- L50 (Logger.print): `Removing SimplyPrint ...`
- L52 (constant): `SimplyPrint Uninstaller`
- L65 (Logger.print): `Exiting SimplyPrint uninstallation ...`
- L72 (constant): `Error during SimplyPrint installation:
`
- L78 (constant): `install`
- L78 (constant): `uninstall`
- L81 (constant): `The following Moonraker instances were found:`
- L126 (constant): `successfully`
- L129 (constant): `installed!`

### kiauh\extensions\spoolman\spoolman.py

**硬编码字符串示例**:

- L41 (constant): `Check if the Spoolman container is running`
- L55 (constant): `Check if Docker is installed and available`
- L104 (constant): `Start the Spoolman container`
- L112 (constant): `Failed to start Spoolman container: `
- L117 (constant): `Update the Spoolman container`
- L120 (constant): `Get the image ID of the Spoolman Docker image`
- L130 (constant): `Failed to get Spoolman Docker image ID`
- L134 (Logger.print): `Pulling latest Spoolman image...`
- L137 (Logger.print): `Tearing down old Spoolman container...`
- L139 (Logger.print): `Spinning up new Spoolman container...`
- L142 (Logger.print): `Removing old Spoolman image...`
- L147 (constant): `Failed to update Spoolman container: `
- L152 (constant): `Stop and remove the Spoolman container`
- L160 (constant): `Failed to tear down Spoolman container: `
- L165 (constant): `Pull the Spoolman Docker image`
- L170 (constant): `Failed to pull Spoolman Docker image: `
- L175 (constant): `Remove the Spoolman Docker image`
- L183 (Logger.print): `Spoolman Docker image not found. Nothing to remove.`
- L189 (constant): `Failed to remove Spoolman Docker image: `

### kiauh\extensions\spoolman\spoolman_extension.py

**硬编码字符串示例**:

- L44 (Logger.print): `Installing Spoolman using Docker...`
- L58 (constant): `Spoolman successfully installed using Docker!`
- L66 (Logger.print): `Updating Spoolman Docker container...`
- L69 (Logger.print): `Spoolman installation not found or incomplete.`
- L76 (Logger.print): `Updating Spoolman container...`
- L82 (constant): `Spoolman Docker container successfully updated!`
- L87 (Logger.print): `Removing Spoolman Docker container...`
- L90 (Logger.print): `Spoolman is not installed. Nothing to remove.`
- L102 (Logger.print): `Removing Spoolman configuration from moonraker.conf...`
- L105 (Logger.print): `Removing Spoolman from moonraker.asvc...`
- L110 (Logger.print): `Stopping and removing Spoolman container...`
- L113 (Logger.print): `Spoolman container removed!`
- L113 (constant): `Spoolman container removed!`
- L115 (Logger.print): `Failed to remove Spoolman container! Please remove it manually.`
- L120 (Logger.print): `Spoolman container and image removed!`
- L120 (constant): `Spoolman container and image removed!`
- L122 (Logger.print): `Failed to remove Spoolman image! Please remove it manually.`
- L135 (constant): `Spoolman data backed up to `
- L136 (Logger.print): `Removing Spoolman directory...`
- L138 (Logger.print): `Spoolman directory removed!`
- L138 (constant): `Spoolman directory removed!`
- L140 (Logger.print): `Failed to remove Spoolman directory! Please remove it manually.`
- L144 (constant): `Failed to backup Spoolman directory: `
- L145 (Logger.print): `Skipping Spoolman directory removal...`
- L149 (constant): `Spoolman successfully removed!`
- L155 (Logger.print): `Setting up Spoolman directories...`
- L163 (Logger.print): `Setting permissions for Spoolman data directory...`
- L165 (Logger.print): `Permissions set!`
- L167 (Logger.print): `Could not set permissions on data directory. This might cause issues.`
- L171 (Logger.print): `Creating Docker Compose file...`
- L173 (Logger.print): `Docker Compose file created!`
- L175 (Logger.print): `Failed to create Docker Compose file!`
- L179 (Logger.print): `Spinning up Spoolman container...`
- L181 (Logger.print): `Spoolman container started!`
- L183 (Logger.print): `Failed to start Spoolman container!`
- L183 (constant): `Failed to start Spoolman container!`
- L186 (Logger.print): `Spoolman integration added to Moonraker!`
- L188 (Logger.print): `Moonraker integration skipped.`
- L194 (Logger.print): `Docker is not installed or not available.`
- L195 (Logger.print): `Please install Docker first: https://docs.docker.com/engine/install/`
- L202 (Logger.print): `Docker Compose is not installed or not available.`
- L251 (Logger.print): `Spoolman is already installed!`
- L251 (constant): `Spoolman is already installed!`
- L254 (Logger.print): `Spoolman container is running but Docker Compose file is missing...`
- L265 (Logger.print): `Docker Compose file exists but container is not running...`
- L273 (constant): `Enable Moonraker integration for Spoolman Docker container`
- L277 (Logger.print): `Adding Spoolman integration to Moonraker...`
- L300 (Logger.print): `Adding Spoolman to moonraker.asvc...`
- L344 (constant): `Spoolman removed from `

### kiauh\extensions\telegram_bot\moonraker_telegram_bot.py

**硬编码字符串示例**:

- L57 (Logger.print): `Creating new Moonraker Telegram Bot Instance ...`
- L71 (constant): `Error creating instance: `
- L74 (constant): `Error creating env file: `
- L84 (constant): `Unable to open `
- L84 (constant): ` - File not found`
- L112 (constant): `Unable to open `
- L112 (constant): ` - File not found`

### kiauh\extensions\telegram_bot\moonraker_telegram_bot_extension.py

**硬编码字符串示例**:

- L41 (Logger.print): `Installing Moonraker Telegram Bot ...`
- L48 (constant): `No Moonraker instances found!`
- L61 (constant): `The following Moonraker instances were found:`
- L126 (Logger.print): `Telegram Bot installation complete!`
- L129 (constant): `Error during installation of Moonraker Telegram Bot:
`
- L133 (Logger.print): `Updating Moonraker Telegram Bot ...`
- L144 (Logger.print): `Removing Moonraker Telegram Bot ...`
- L153 (constant): `update_manager moonraker-telegram-bot`
- L156 (constant): `Error during removal of Moonraker Telegram Bot:
`
- L158 (Logger.print): `Moonraker Telegram Bot removed!`
- L158 (constant): `Moonraker Telegram Bot removed!`
- L174 (constant): `update_manager moonraker-telegram-bot`
- L182 (constant): `install_script`
- L204 (constant): `Unable to delete '`
- L214 (constant): `Unable to delete '`
- L221 (Logger.print): `No Moonraker Telegram Bot logs found. Skipped ...`
- L225 (constant): `Remove '`
- L204 (fstring): `Unable to delete`
- L214 (fstring): `Unable to delete`
- L225 (fstring): `Remove`

### kiauh\main.py

**硬编码字符串示例**:

- L52 (constant): `未知`
- L52 (constant): `未知`
- L62 (constant): `network_google_error`

**translate() 调用**:

- L51: `welcome`
- L52: `system_language`
- L58: `network_google_ok`
- L60: `network_google_fail`
- L62: `network_google_error`
- L70: `happy_printing`

**TRANSLATIONS 查找**:

- L34: `<non-literal>`

### kiauh\procedures\switch_repo.py

**硬编码字符串示例**:

- L98 (constant): `Failed to recreate virtualenv for `
- L105 (constant): `Error during backup of repository: `
- L111 (constant): `Error during repository switch: `
- L112 (constant): `Restoring last backup of `
- L139 (constant): `Unable to restore backup of `
- L149 (constant): ` successfully!`
- L151 (constant): `Error restoring backup: `

### kiauh\procedures\system.py

**硬编码字符串示例**:

- L28 (constant): `Changing the hostname of this system allows you to access an installed webinterface by simply typing the hostname like this in the browser:`
- L37 (constant): `CHANGE SYSTEM HOSTNAME`
- L53 (constant): `Enter the new hostname`
- L57 (Logger.print): `Aborting hostname change ...`
- L61 (Logger.print): `Changing hostname ...`
- L63 (Logger.print): `Checking for dependencies ...`
- L67 (Logger.print): `Creating backup of hosts file ...`
- L92 (Logger.print): `Writing new hostname to /etc/hosts ...`
- L98 (Logger.print): `New hostname successfully configured!`
- L99 (Logger.print): `Remember to reboot for the changes to take effect!
`
- L102 (constant): `Error during change hostname procedure: `
- L56 (fstring): `Change the hostname to`

### kiauh\utils\common.py

**硬编码字符串示例**:

- L88 (Logger.print): `Installing dependencies ...`
- L89 (Logger.print): `The following packages need installation:`
- L89 (constant): `The following packages need installation:`
- L162 (Logger.print): `Unable to find directory to backup!`
- L162 (constant): `Unable to find directory to backup!`
- L163 (Logger.print): `Are there no Klipper instances installed?`
- L175 (constant): `
    Helper method to check if a Moonraker instance exists
    :param name: Optional name of an installer where the check is performed
    :return: True if at least one Moonraker instance exists, False otherwise
    `
- L183 (constant): ` requires Moonraker to be installed`
- L185 (constant): `A Moonraker installation is required`
- L192 (constant): `No Moonraker instances found!`

### kiauh\utils\config_utils.py

**硬编码字符串示例**:

- L38 (constant): `' not found!`
- L44 (Logger.print): `Section already exist. Skipped ...`
- L55 (Logger.print): `OK!`
- L78 (Logger.print): `OK!`
- L90 (constant): `' not found!`
- L96 (Logger.print): `Section does not exist. Skipped ...`
- L103 (Logger.print): `OK!`
- L87 (fstring): `Remove section`

### kiauh\utils\fs_utils.py

**硬编码字符串示例**:

- L53 (constant): `Failed to create symlink: `
- L73 (constant): `' was successfully removed!`
- L76 (constant): `Error removing file '`
- L87 (constant): `Cannot remove file `
- L105 (constant): `' was successfully removed!`
- L108 (constant): `Unable to delete '`
- L110 (Logger.print): `Trying to remove with sudo ...`
- L112 (constant): `' was successfully removed!`
- L115 (constant): `Error deleting '`
- L116 (Logger.print): `Remove this directory manually!`
- L116 (constant): `Remove this directory manually!`
- L139 (constant): `Error creating directories: `
- L76 (fstring): `Error removing file`
- L108 (fstring): `Unable to delete`
- L115 (fstring): `Error deleting`

### kiauh\utils\git_utils.py

**硬编码字符串示例**:

- L43 (Logger.print): `Skip cloning of repository ...`
- L57 (constant): `Error removing existing repository: `
- L58 (constant): `Error removing existing repository: `
- L68 (Logger.print): `Updating repository ...`
- L166 (constant): `Error while processing the response: `
- L200 (Logger.print): `Error while getting the latest unstable tag`
- L200 (constant): `Error while getting the latest unstable tag`
- L278 (Logger.print): `Clone successful!`
- L278 (constant): `Clone successful!`
- L280 (constant): `Unknown error`
- L281 (constant): `Error cloning repository `
- L294 (Logger.print): `Checkout successful!`
- L294 (constant): `Checkout successful!`
- L296 (constant): `Error checking out branch `
- L306 (constant): `Error on git pull: `
- L317 (Logger.print): `Do not continue if you have ongoing prints!`
- L319 (constant): `All currently running `
- L326 (Logger.print): `Aborting roll back ...`
- L336 (constant): `An error occured during repo rollback:
`
- L342 (constant): `
    Get the remote repository URL for a git repository
    :param repo_dir: Path to the git repository
    :return: URL of the remote repository or None if not found
    `
- L37 (fstring): `Cloning repository from`

### kiauh\utils\input_utils.py

**硬编码字符串示例**:

- L112 (Logger.print): `Input must not be empty!`
- L116 (Logger.print): `This value is already in use/reserved.`
- L145 (Logger.print): `Invalid option! Please select a valid option.`

### kiauh\utils\sys_utils.py

**硬编码字符串示例**:

- L39 (constant): `reset-failed`
- L47 (constant): `
    Kills the application |
    :param opt_err_msg: an optional, additional error message
    :return: None
    `
- L55 (Logger.print): `A critical error has occured. KIAUH was terminated.`
- L67 (Logger.print): `Versioncheck failed!`
- L67 (constant): `Versioncheck failed!`
- L110 (Logger.print): `Set up Python virtual environment ...`
- L123 (Logger.print): `Setup of virtualenv successful!`
- L123 (constant): `Setup of virtualenv successful!`
- L126 (constant): `Error setting up virtualenv:
`
- L132 (Logger.print): `Virtualenv still exists after deletion.`
- L137 (Logger.print): `Skipping re-creation of virtualenv ...`
- L144 (constant): `Error removing existing virtualenv: `
- L155 (Logger.print): `Updating pip ...`
- L163 (constant): `install`
- L167 (Logger.print): `Updating pip failed!`
- L170 (Logger.print): `Updating pip successful!`
- L187 (Logger.print): `Installing Python requirements ...`
- L190 (constant): `install`
- L200 (Logger.print): `Installing Python requirements successful!`
- L216 (Logger.print): `Installing Python requirements ...`
- L219 (constant): `install`
- L229 (Logger.print): `Installing Python requirements successful!`
- L238 (constant): `
    Updates the systems package list |
    :param silent: Log info to the console or not
    :param rls_info_change: Flag for "--allow-releaseinfo-change"
    :return: None
    `
- L260 (Logger.print): `Updating package list...`
- L263 (constant): `update`
- L265 (constant): `--allow-releaseinfo-change`
- L270 (Logger.print): `Updating system package list failed!`
- L270 (constant): `Updating system package list failed!`
- L273 (Logger.print): `System package list update successful!`
- L273 (constant): `System package list update successful!`
- L275 (constant): `Error updating system package list:
`
- L295 (constant): `Error reading upgradable packages: `
- L299 (constant): `
    Checks the system for installed packages |
    :param packages: List of strings of package names
    :return: A list containing the names of packages that are not installed
    `
- L313 (constant): `installed`
- L320 (constant): `
    Installs a list of system packages |
    :param packages: List of system package names
    :return: None
    `
- L326 (constant): `install`
- L331 (Logger.print): `Packages successfully installed.`
- L333 (constant): `Error installing packages:
`
- L338 (constant): `
    Updates a list of system packages |
    :param packages: List of system package names
    :return: None
    `
- L349 (Logger.print): `Packages successfully upgraded.`
- L351 (constant): `Error upgrading packages:
`
- L393 (constant): `Download failed! URL error occured: `
- L396 (constant): `Download failed! An error occured: `
- L431 (Logger.print): `Granting NGINX the required permissions ...`
- L433 (Logger.print): `Permissions granted.`
- L446 (Logger.print): `OK!`
- L448 (constant): `Failed to `
- L457 (constant): `Failed to run `
- L536 (constant): `Error creating env file: `
- L560 (constant): `reset-failed`

