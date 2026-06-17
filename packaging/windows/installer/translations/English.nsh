;
;  SPDX-License-Identifier: GPL-3.0-or-later
;

!define CURRENT_LANG ${LANG_ENGLISH}

# Strings to show in the installation log:
LangString RemovingShellEx ${CURRENT_LANG} "Removing Minerva Shell Integration..."
LangString RemoveShellExFailed ${CURRENT_LANG} "Failed to remove Minerva Shell Integration."
LangString RemoveShellExDone ${CURRENT_LANG} "Minerva Shell Integration removed."
LangString RemovingOldVer ${CURRENT_LANG} "Removing previous version..."
LangString RemoveOldVerFailed ${CURRENT_LANG} "Failed to remove previous version of Minerva."
LangString RemoveOldVerDone ${CURRENT_LANG} "Previous version removed."

# Strings for the component selection dialog:
LangString SectionRemoveOldVer ${CURRENT_LANG} "Remove Old Version"
LangString SectionRemoveOldVerDesc ${CURRENT_LANG} "Remove previously installed Minerva $MinervaNsisVersion ($MinervaNsisBitness-bit)."
LangString SectionShellEx ${CURRENT_LANG} "Shell Integration"
LangString SectionShellExDesc ${CURRENT_LANG} "Shell Extension component to provide thumbnails and file properties display for Minerva files.$\r$\n$\r$\nVersion: ${KRITASHELLEX_VERSION}"
LangString SectionMainDesc ${CURRENT_LANG} "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}$\r$\n$\r$\nVersion: ${MINERVA2D_VERSION}"

# Main dialog strings:
LangString SetupLangPrompt ${CURRENT_LANG} "Choose the language to be used for the setup process:"
LangString ShellExLicensePageHeader ${CURRENT_LANG} "License Agreement (Minerva Shell Extension)"
LangString ConfirmInstallPageHeader ${CURRENT_LANG} "Confirm Installation"
LangString ConfirmInstallPageDesc ${CURRENT_LANG} "Confirm installation of ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}."
LangString DesktopIconPageDesc2 ${CURRENT_LANG} "You can choose whether to create a shortcut icon on the desktop for launching Minerva:"
LangString DesktopIconPageCheckbox ${CURRENT_LANG} "Create a desktop icon"
LangString ConfirmInstallPageDesc2 ${CURRENT_LANG} "Setup is ready to install ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}. You may go back to review the install options before you continue.$\r$\n$\r$\n$_CLICK"

# Misc. message prompts:
LangString MsgRequireWin7 ${CURRENT_LANG} "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY} requires Windows 7 or above."
LangString Msg64bitOn32bit ${CURRENT_LANG} "You are running 32-bit Windows, but this installer installs Minerva 64-bit which can only be installed on 64-bit Windows. Please download the 32-bit version on https://minerva2d.org/"
LangString Msg32bitOn64bit ${CURRENT_LANG} "You are trying to install 32-bit Minerva on 64-bit Windows. You are strongly recommended to install the 64-bit version of Minerva instead since it offers better performance.$\nYou can download the 64-bit version on https://minerva2d.org/$\n$\nDo you still wish to install the 32-bit version of Minerva?"
# These prompts are used for when Minerva 2.9 or earlier, or the 3.0 alpha 1 MSI version is installed.
LangString MsgAncientVerMustBeRemoved ${CURRENT_LANG} "An ancient version of Minerva is detected. This program will now attempt to remove any old versions of Minerva.$\nDo you wish to continue?"
LangString MsgMinerva3alpha1RemoveFailed ${CURRENT_LANG} "Failed to remove Minerva 3.0 Alpha 1."
LangString MsgMinerva2msi32bitRemoveFailed ${CURRENT_LANG} "Failed to remove old Minerva (32-bit)."
LangString MsgMinerva2msi64bitRemoveFailed ${CURRENT_LANG} "Failed to remove old Minerva (64-bit)."
#
LangString MsgMinervaSameVerReinstall ${CURRENT_LANG} "It appears that ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY} is already installed.$\nThis setup will reinstall it."
LangString MsgMinerva3264bitSwap ${CURRENT_LANG} "It appears that Minerva $MinervaNsisBitness-bit ($MinervaNsisVersion) is currently installed. This setup will replace it with the ${MINERVA2D_INSTALLER_BITNESS}-bit version of Minerva ${MINERVA2D_VERSION_DISPLAY}."
LangString MsgMinervaNewerAlreadyInstalled ${CURRENT_LANG} "It appears that a newer version of Minerva $MinervaNsisBitness-bit ($MinervaNsisVersion) is currently installed. If you want to downgrade Minerva to ${MINERVA2D_VERSION_DISPLAY}, please uninstall the newer version manually before running this setup."
LangString MsgMinervaRunning ${CURRENT_LANG} "Minerva appears to be running. Please close Minerva before running this installer."
LangString MsgUninstallMinervaRunning ${CURRENT_LANG} "Minerva appears to be running. Please close Minerva before uninstalling."

!undef CURRENT_LANG
