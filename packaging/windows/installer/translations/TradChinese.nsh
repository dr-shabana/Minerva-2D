;
;  SPDX-License-Identifier: GPL-3.0-or-later
;

!define CURRENT_LANG ${LANG_TRADCHINESE}

# Strings to show in the installation log:
LangString RemovingShellEx ${CURRENT_LANG} "正在移除 Minerva 系統介面整合元件..."
LangString RemoveShellExFailed ${CURRENT_LANG} "無法成功移除 Minerva 系統介面整合元件。"
LangString RemoveShellExDone ${CURRENT_LANG} "已移除 Minerva 系統介面整合元件。"
LangString RemovingOldVer ${CURRENT_LANG} "正在解除安裝先前版本..."
LangString RemoveOldVerFailed ${CURRENT_LANG} "無法成功解除安裝先前版本的 Minerva。"
LangString RemoveOldVerDone ${CURRENT_LANG} "已解除安裝先前版本。"

# Strings for the component selection dialog:
LangString SectionRemoveOldVer ${CURRENT_LANG} "移除先前版本"
LangString SectionRemoveOldVerDesc ${CURRENT_LANG} "解除安裝先前曾安裝的 Minerva $MinervaNsisVersion ($MinervaNsisBitness-bit)."
LangString SectionShellEx ${CURRENT_LANG} "系統介面整合"
LangString SectionShellExDesc ${CURRENT_LANG} "安裝整合元件 (Shell Extension) 以在 Window 檔案總管中顯示 Minerva 檔案的縮圖和屬性資訊。$\r$\n$\r$\n版本: ${KRITASHELLEX_VERSION}"
LangString SectionMainDesc ${CURRENT_LANG} "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}$\r$\n$\r$\n版本: ${MINERVA2D_VERSION}"

# Main dialog strings:
LangString SetupLangPrompt ${CURRENT_LANG} "請選擇安裝過程使用的語言:"
LangString ShellExLicensePageHeader ${CURRENT_LANG} "授權協議 (Minerva 系統介面整合元件)"
LangString ConfirmInstallPageHeader ${CURRENT_LANG} "確認安裝"
LangString ConfirmInstallPageDesc ${CURRENT_LANG} "確認安裝 ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}。"
LangString DesktopIconPageDesc2 ${CURRENT_LANG} "你可以選擇要否在桌面上建立開啟 Minerva 的捷徑:"
LangString DesktopIconPageCheckbox ${CURRENT_LANG} "在桌面建立捷徑"
LangString ConfirmInstallPageDesc2 ${CURRENT_LANG} "本安裝程式已準備好在電腦安裝 ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}。如有需要，你可以返回先前的頁面檢查安裝選項。$\r$\n$\r$\n$_CLICK"

# Misc. message prompts:
LangString MsgRequireWin7 ${CURRENT_LANG} "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY} 只支援 Windows 7 或以上版本。"
LangString Msg64bitOn32bit ${CURRENT_LANG} "此電腦正在執行32位元版本的 Windows，但本安裝程式提供64位元版本的 Minerva 只能在64位元版本的 Windows 上使用。請到 https://minerva2d.org/ 下載32位元版本的 Minerva。"
LangString Msg32bitOn64bit ${CURRENT_LANG} "你正嘗試在64位元版本的 Windows 上安裝32位元版本的 Minerva。本安裝程式建議你安裝效能更高的64位元版本的 Minerva。$\n請到 https://minerva2d.org/ 下載64位元版本的 Minerva。$\n$\n你仍要安裝32位元版本的 Minerva嗎？"
# These prompts are used for when Minerva 2.9 or earlier, or the 3.0 alpha 1 MSI version is installed.
LangString MsgAncientVerMustBeRemoved ${CURRENT_LANG} "發現電腦上安裝有舊版本的 Minerva。本安裝程式會先嘗試將其解除安裝。$\n你確定要繼續嗎？"
LangString MsgMinerva3alpha1RemoveFailed ${CURRENT_LANG} "無法成功解除安裝 Minerva 3.0 Alpha 1。"
LangString MsgMinerva2msi32bitRemoveFailed ${CURRENT_LANG} "無法成功解除安裝舊版 Minerva (32-bit)。"
LangString MsgMinerva2msi64bitRemoveFailed ${CURRENT_LANG} "無法成功解除安裝舊版 Minerva (64-bit)。"
#
LangString MsgMinervaSameVerReinstall ${CURRENT_LANG} "發現電腦上已安裝有 ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}。$\n本安裝程式會重新安裝此版本的 Minerva。"
LangString MsgMinerva3264bitSwap ${CURRENT_LANG} "發現電腦上已安裝有$MinervaNsisBitness位元版本的 Minerva ($MinervaNsisVersion)。本安裝程式會以${MINERVA2D_INSTALLER_BITNESS}位元版本的 Minerva ${MINERVA2D_VERSION_DISPLAY} 將其取代。"
LangString MsgMinervaNewerAlreadyInstalled ${CURRENT_LANG} "發現電腦上已安裝有$MinervaNsisBitness位元版本的 Minerva ($MinervaNsisVersion)。如需安裝較舊版本的 Minerva (${MINERVA2D_VERSION_DISPLAY})，請先自行解除安裝現有版本的 Minerva。"
LangString MsgMinervaRunning ${CURRENT_LANG} "發現 Minerva 正在執行中。使用本安裝程式前請先退出 Minerva。"
LangString MsgUninstallMinervaRunning ${CURRENT_LANG} "發現 Minerva 正在執行中。解除安裝前請先退出 Minerva。"

!undef CURRENT_LANG
