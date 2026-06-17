!ifndef MINERVA2D_INSTALLER_32 & MINERVA2D_INSTALLER_64
	!error "Either one of MINERVA2D_INSTALLER_32 or MINERVA2D_INSTALLER_64 must be defined."
!endif
!ifdef MINERVA2D_INSTALLER_32 & MINERVA2D_INSTALLER_64
	!error "Only one of MINERVA2D_INSTALLER_32 or MINERVA2D_INSTALLER_64 should be defined."
!endif

!ifndef MINERVA2D_PACKAGE_ROOT
	!error "MINERVA2D_PACKAGE_ROOT should be defined and point to the root of the package files."
!endif

!ifdef MINERVA2D_INSTALLER_64
	!define MINERVA2D_INSTALLER_BITNESS 64
!else
	!define MINERVA2D_INSTALLER_BITNESS 32
!endif

Unicode true
# Enabling DPI awareness creates awful CJK text in some sizes, so don't enable it.
ManifestDPIAware false

# Minerva constants (can be overridden in command line params)
!define /ifndef MINERVA2D_VERSION "0.0.0.0"
!define /ifndef MINERVA2D_VERSION_DISPLAY "test-version"
#!define /ifndef MINERVA2D_VERSION_GIT ""
!define /ifndef MINERVA2D_INSTALLER_OUTPUT_DIR ""
!ifdef MINERVA2D_INSTALLER_64
	!define /ifndef MINERVA2D_INSTALLER_OUTPUT_NAME "minerva2d_x64_setup.exe"
!else
	!define /ifndef MINERVA2D_INSTALLER_OUTPUT_NAME "minerva2d_x86_setup.exe"
!endif

# Minerva constants (fixed)
!if "${MINERVA2D_INSTALLER_OUTPUT_DIR}" == ""
	!define MINERVA2D_INSTALLER_OUTPUT "${MINERVA2D_INSTALLER_OUTPUT_NAME}"
!else
	!define MINERVA2D_INSTALLER_OUTPUT "${MINERVA2D_INSTALLER_OUTPUT_DIR}\${MINERVA2D_INSTALLER_OUTPUT_NAME}"
!endif
!define KRTIA_PUBLISHER "Minerva Foundation"
!ifdef MINERVA2D_INSTALLER_64
	!define MINERVA2D_PRODUCTNAME "Minerva (x64)"
	!define MINERVA2D_UNINSTALL_REGKEY "Minerva_x64"
!else
	!define MINERVA2D_PRODUCTNAME "Minerva (x86)"
	!define MINERVA2D_UNINSTALL_REGKEY "Minerva_x86"
!endif

VIProductVersion "${MINERVA2D_VERSION}"
VIAddVersionKey "CompanyName" "${KRTIA_PUBLISHER}"
VIAddVersionKey "FileDescription" "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY} Setup"
VIAddVersionKey "FileVersion" "${MINERVA2D_VERSION}"
VIAddVersionKey "InternalName" "${MINERVA2D_INSTALLER_OUTPUT_NAME}"
VIAddVersionKey "LegalCopyright" "${KRTIA_PUBLISHER}"
VIAddVersionKey "OriginalFileName" "${MINERVA2D_INSTALLER_OUTPUT_NAME}"
VIAddVersionKey "ProductName" "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY} Setup"
VIAddVersionKey "ProductVersion" "${MINERVA2D_VERSION}"

BrandingText "[NSIS ${NSIS_VERSION}]  ${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION}"

Name "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}"
OutFile ${MINERVA2D_INSTALLER_OUTPUT}
!ifdef MINERVA2D_INSTALLER_64
	InstallDir "$PROGRAMFILES64\Minerva (x64)"
!else
	InstallDir "$PROGRAMFILES32\Minerva (x86)"
!endif
XPstyle on

ShowInstDetails show
ShowUninstDetails show

Var MinervaStartMenuFolder
Var CreateDesktopIcon

!include MUI2.nsh

!define MUI_FINISHPAGE_NOAUTOCLOSE

# Installer Pages
!insertmacro MUI_PAGE_WELCOME
!define MUI_LICENSEPAGE_CHECKBOX
!insertmacro MUI_PAGE_LICENSE "license_gpl-3.0.rtf"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_COMPONENTS
!define MUI_PAGE_CUSTOMFUNCTION_PRE  func_ShellExLicensePage_Init
!define MUI_PAGE_HEADER_TEXT "$(ShellExLicensePageHeader)"
!insertmacro MUI_PAGE_LICENSE "license.rtf"
!define MUI_STARTMENUPAGE_DEFAULTFOLDER "Minerva"
!define MUI_STARTMENUPAGE_REGISTRY_ROOT HKLM
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\Minerva"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "StartMenuFolder"
!define MUI_STARTMENUPAGE_NODISABLE
!insertmacro MUI_PAGE_STARTMENU Minerva $MinervaStartMenuFolder
Page Custom func_BeforeInstallPage_Init
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstaller Pages
!define MUI_PAGE_CUSTOMFUNCTION_PRE un.func_UnintallFirstpage_Init
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# Languages
!insertmacro MUI_LANGUAGE "English"
!insertmacro MUI_LANGUAGE "TradChinese"
!insertmacro MUI_LANGUAGE "SimpChinese"

!include Sections.nsh
!include LogicLib.nsh
!include x64.nsh
!include WinVer.nsh
!include WordFunc.nsh

!define MINERVA2D_SHELLEX_DIR "$INSTDIR\shellex"

!include "include\FileExists2.nsh"
!include "include\IsFileInUse.nsh"
!include "minerva2d_versions_detect.nsh"
!include "minerva2d_shell_integration.nsh"

Var MinervaMsiProductX86
Var MinervaMsiProductX64
Var MinervaNsisVersion
Var MinervaNsisBitness
Var MinervaNsisInstallLocation

Var PrevShellExInstallLocation
Var PrevShellExStandalone

Var UninstallShellExStandalone

Section "-Remove_shellex" SEC_remove_shellex
	${If} $PrevShellExInstallLocation != ""
	${AndIf} $PrevShellExStandalone == 1
	${AndIf} $MinervaNsisVersion == ""
	${AndIf} ${FileExists} "$PrevShellExInstallLocation\uninstall.exe"
		push $R0
		DetailPrint "$(RemovingShellEx)"
		SetDetailsPrint listonly
		ExecWait "$PrevShellExInstallLocation\uninstall.exe /S _?=$PrevShellExInstallLocation" $R0
		${If} $R0 != 0
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONSTOP "$(RemoveShellExFailed)"
			${EndIf}
			SetDetailsPrint both
			DetailPrint "$(RemoveShellExFailed)"
			Abort
		${EndIf}
		Delete "$PrevShellExInstallLocation\uninstall.exe"
		RMDir /REBOOTOK "$PrevShellExInstallLocation"
		SetRebootFlag false
		SetDetailsPrint lastused
		DetailPrint "$(RemoveShellExDone)"
		pop $R0
	${EndIf}
SectionEnd

Section "$(SectionRemoveOldVer)" SEC_remove_old_version
	${If} $MinervaNsisInstallLocation != ""
	${AndIf} ${FileExists} "$MinervaNsisInstallLocation\uninstall.exe"
		push $R0
		DetailPrint "$(RemovingOldVer)"
		SetDetailsPrint listonly
		ExecWait "$MinervaNsisInstallLocation\uninstall.exe /S _?=$MinervaNsisInstallLocation" $R0
		${If} $R0 != 0
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONSTOP "$(RemoveOldVerFailed)"
			${EndIf}
			SetDetailsPrint both
			DetailPrint "$(RemoveOldVerFailed)"
			Abort
		${EndIf}
		Delete "$MinervaNsisInstallLocation\uninstall.exe"
		RMDir /REBOOTOK "$MinervaNsisInstallLocation"
		SetRebootFlag false
		SetDetailsPrint lastused
		DetailPrint "$(RemoveOldVerDone)"
		pop $R0
	${EndIf}
SectionEnd

Section "-Thing"
	SetOutPath $INSTDIR
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "DisplayName" "${MINERVA2D_PRODUCTNAME} ${MINERVA2D_VERSION_DISPLAY}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
	WriteUninstaller $INSTDIR\uninstall.exe
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "DisplayVersion" "${MINERVA2D_VERSION}"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "DisplayIcon" "$\"$INSTDIR\shellex\minerva2d.ico$\",0"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "URLInfoAbout" "https://minerva2d.org/"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "InstallLocation" "$INSTDIR"
	WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                 "Publisher" "${KRTIA_PUBLISHER}"
	#WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	#                   "EstimatedSize" 250000
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                   "NoModify" 1
	WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}" \
	                   "NoRepair" 1
	# Registry entries for version recognition
	#   InstallLocation:
	#     Where krita is installed
	WriteRegStr HKLM "Software\Minerva" \
	                 "InstallLocation" "$INSTDIR"
	#   Version:
	#     Version of Minerva
	WriteRegStr HKLM "Software\Minerva" \
	                 "Version" "${MINERVA2D_VERSION}"
	#   x64:
	#     Set to 1 for 64-bit Minerva, can be missing for 32-bit Minerva
!ifdef MINERVA2D_INSTALLER_64
	WriteRegDWORD HKLM "Software\Minerva" \
	                   "x64" 1
!else
	DeleteRegValue HKLM "Software\Minerva" "x64"
!endif
	#   InstallerLanguage:
	#     Language used by the installer (to be re-used for the uninstaller)
	WriteRegStr HKLM "Software\Minerva" \
	                 "InstallerLanguage" "$LANGUAGE"
	#   StartMenuFolder:
	#     Start Menu Folder
	#     Handled by Modern UI 2.0 MUI_PAGE_STARTMENU
SectionEnd

Section "${MINERVA2D_PRODUCTNAME}" SEC_product_main
	# TODO: Maybe switch to explicit file list?
	File /r ${MINERVA2D_PACKAGE_ROOT}\bin
	File /r ${MINERVA2D_PACKAGE_ROOT}\lib
	File /r ${MINERVA2D_PACKAGE_ROOT}\share
	File /r ${MINERVA2D_PACKAGE_ROOT}\python
SectionEnd

Section "-Main_associate"
	CreateDirectory ${MINERVA2D_SHELLEX_DIR}
	${Minerva_RegisterFileAssociation} "$INSTDIR\bin\minerva2d.exe"
SectionEnd

Section "-Main_Shortcuts"
	# Placing this after Minerva_RegisterFileAssociation to get the icon
	!insertmacro MUI_STARTMENU_WRITE_BEGIN Minerva
		CreateDirectory "$SMPROGRAMS\$MinervaStartMenuFolder"
		CreateShortcut "$SMPROGRAMS\$MinervaStartMenuFolder\${MINERVA2D_PRODUCTNAME}.lnk" "$INSTDIR\bin\minerva2d.exe" "" "$INSTDIR\shellex\minerva2d.ico" 0
	!insertmacro MUI_STARTMENU_WRITE_END
	${If} $CreateDesktopIcon == 1
		# For the desktop icon, keep the name short and omit version info
		CreateShortcut "$DESKTOP\Minerva.lnk" "$INSTDIR\bin\minerva2d.exe" "" "$INSTDIR\shellex\minerva2d.ico" 0
	${EndIf}
SectionEnd

Section "$(SectionShellEx)" SEC_shellex
	${If} ${RunningX64}
		${Minerva_RegisterComComonents} 64
	${EndIf}
	${Minerva_RegisterComComonents} 32

	${Minerva_RegisterShellExtension}

	#   ShellExtension\InstallLocation:
	#     Where the shell extension is installed
	#     If installed by Minerva installer, this must point to shellex sub-dir
	WriteRegStr HKLM "Software\Minerva\ShellExtension" \
	                 "InstallLocation" "$INSTDIR\shellex"
	#   ShellExtension\Version:
	#     Version of the shell extension
	WriteRegStr HKLM "Software\Minerva\ShellExtension" \
	                 "Version" "${KRITASHELLEX_VERSION}"
	#   ShellExtension\Standalone:
	#     0 = Installed by Minerva installer
	#     1 = Standalone installer
	WriteRegDWORD HKLM "Software\Minerva\ShellExtension" \
	                   "Standalone" 0
	#   ShellExtension\MinervaExePath:
	#     Path to minerva2d.exe as specified by user or by Minerva installer
	#     Empty if not specified
	WriteRegStr HKLM "Software\Minerva\ShellExtension" \
	                 "MinervaExePath" "$INSTDIR\bin\minerva2d.exe"
SectionEnd

Section "-Main_refreshShell"
	${RefreshShell}
SectionEnd

Section "-Main_MSVC"
!ifdef MINERVA2D_INSTALLER_64
	${If} ${FileExists} "$INSTDIR\bin\vc_redist.x64.exe"
		ExecWait "$INSTDIR\bin\vc_redist.x64.exe /install /quiet /norestart"
		Delete "$INSTDIR\bin\vc_redist.x64.exe"
	${Endif}
!else
	${If} ${FileExists} "$INSTDIR\bin\vc_redist.exe"
		ExecWait "$INSTDIR\bin\vc_redist.x86.exe /install /quiet /norestart"
		Delete "$INSTDIR\bin\vc_redist.x86.exe"
	${Endif}
!endif
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
	#!insertmacro MUI_DESCRIPTION_TEXT ${SEC_remove_shellex} "Remove previously installed Minerva Shell Integration."
	!insertmacro MUI_DESCRIPTION_TEXT ${SEC_remove_old_version} "$(SectionRemoveOldVerDesc)"
	!insertmacro MUI_DESCRIPTION_TEXT ${SEC_product_main} "$(SectionMainDesc)"
	!insertmacro MUI_DESCRIPTION_TEXT ${SEC_shellex} "$(SectionShellExDesc)"
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Section "un.$(SectionShellEx)"
	${If} $UninstallShellExStandalone == 1
		push $R0
		DetailPrint "$(RemovingShellEx)"
		SetDetailsPrint listonly
		ExecWait "$INSTDIR\shellex\uninstall.exe /S _?=$INSTDIR\shellex" $R0
		${If} $R0 != 0
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONSTOP "$(RemoveShellExFailed)"
			${EndIf}
			SetDetailsPrint lastused
			SetDetailsPrint both
			DetailPrint "$(RemoveShellExFailed)"
		${EndIf}
		Delete "$INSTDIR\shellex\uninstall.exe"
		RMDir /REBOOTOK "$INSTDIR\shellex"
		SetDetailsPrint lastused
		DetailPrint "$(RemoveShellExDone)"
		pop $R0
	${Else}
		${Minerva_UnregisterShellExtension}

		${If} ${RunningX64}
			${Minerva_UnregisterComComonents} 64
		${EndIf}
		${Minerva_UnregisterComComonents} 32
	${EndIf}
SectionEnd

Section "un.Main_associate"
	# TODO: Conditional, use install log
	${If} $UninstallShellExStandalone != 1
		${Minerva_UnregisterFileAssociation}
	${EndIf}
SectionEnd

Section "un.Main_Shortcuts"
	Delete "$DESKTOP\Minerva.lnk"
	!insertmacro MUI_STARTMENU_GETFOLDER Minerva $MinervaStartMenuFolder
	Delete "$SMPROGRAMS\$MinervaStartMenuFolder\${MINERVA2D_PRODUCTNAME}.lnk"
	RMDir "$SMPROGRAMS\$MinervaStartMenuFolder"
SectionEnd

Section "un.${MINERVA2D_PRODUCTNAME}"
	# TODO: Maybe switch to explicit file list or some sort of install log?
	RMDir /r $INSTDIR\bin
	RMDir /r $INSTDIR\lib
	RMDir /r $INSTDIR\share
	RMDir /r $INSTDIR\python
SectionEnd

Section "un.Thing"
	RMDir /REBOOTOK $INSTDIR\shellex
	DeleteRegKey HKLM "Software\Minerva"
	DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MINERVA2D_UNINSTALL_REGKEY}"
	Delete $INSTDIR\uninstall.exe
	RMDir /REBOOTOK $INSTDIR
SectionEnd

Section "un.Main_refreshShell"
	${RefreshShell}
SectionEnd

Function .onInit
	SetShellVarContext all
	!insertmacro SetSectionFlag ${SEC_product_main} ${SF_RO}
	!insertmacro SetSectionFlag ${SEC_product_main} ${SF_BOLD}
	!insertmacro SetSectionFlag ${SEC_remove_old_version} ${SF_RO}
	StrCpy $CreateDesktopIcon 1 # Create desktop icon by default
	${IfNot} ${AtLeastWin7}
		${IfNot} ${Silent}
			MessageBox MB_OK|MB_ICONSTOP "$(MsgRequireWin7)"
		${EndIf}
		Abort
	${EndIf}

	${IfNot} ${Silent}
		# Language selection, seems that the order is predefined.
		Push "" # This value is for languages auto count
		Push ${LANG_ENGLISH}
		Push English
		Push ${LANG_TRADCHINESE}
		Push "繁體中文"
		Push ${LANG_SIMPCHINESE}
		Push "简体中文"
		Push A # = auto count languages
		LangDLL::LangDialog "$(^SetupCaption)" "$(SetupLangPrompt)"
		Pop $LANGUAGE
		${If} $LANGUAGE == "cancel"
			Abort
		${Endif}
	${EndIf}

!ifdef MINERVA2D_INSTALLER_64
	${If} ${RunningX64}
		SetRegView 64
	${Else}
		${IfNot} ${Silent}
			MessageBox MB_OK|MB_ICONSTOP "$(Msg64bitOn32bit)"
		${EndIf}
		Abort
	${Endif}
!else
	${If} ${RunningX64}
		SetRegView 64
		${IfNot} ${Silent}
			MessageBox MB_YESNO|MB_ICONEXCLAMATION "$(Msg32bitOn64bit)" \
			           /SD IDYES \
			           IDYES lbl_allow32on64
			Abort
		${EndIf}
		lbl_allow32on64:
	${Endif}
!endif

	# Detect ancient Minerva versions
	${DetectMinervaMsi32bit} $MinervaMsiProductX86
	${If} ${RunningX64}
		${DetectMinervaMsi64bit} $MinervaMsiProductX64
	${EndIf}
	${If} $MinervaMsiProductX86 != ""
	${OrIf} $MinervaMsiProductX64 != ""
		${IfNot} ${Silent}
			MessageBox MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON1 "$(MsgAncientVerMustBeRemoved)" \
						/SD IDYES \
						IDYES lbl_removeAncientVer
			Abort
		${EndIf}
		lbl_removeAncientVer:
		${If} $MinervaMsiProductX64 != ""
			push $R0
			${MsiUninstall} $MinervaMsiProductX64 $R0
			${If} $R0 != 0
				${IfNot} ${Silent}
					${IfMinervaMsi3Alpha} $MinervaMsiProductX64
						MessageBox MB_OK|MB_ICONSTOP "$(MsgMinerva3alpha1RemoveFailed)"
					${Else}
						MessageBox MB_OK|MB_ICONSTOP "$(MsgMinerva2msi64bitRemoveFailed)"
					${EndIf}
				${EndIf}
				Abort
			${EndIf}
			pop $R0
			StrCpy $MinervaMsiProductX64 ""
		${EndIf}
		${If} $MinervaMsiProductX86 != ""
			push $R0
			${MsiUninstall} $MinervaMsiProductX86 $R0
			${If} $R0 != 0
				${IfNot} ${Silent}
					MessageBox MB_OK|MB_ICONSTOP "$(MsgMinerva2msi32bitRemoveFailed)"
				${EndIf}
				Abort
			${EndIf}
			pop $R0
			StrCpy $MinervaMsiProductX86 ""
		${EndIf}
	${EndIf}

	${DetectMinervaNsis} $MinervaNsisVersion $MinervaNsisBitness $MinervaNsisInstallLocation
	${If} $MinervaNsisVersion != ""
		push $R0
		${If} $MinervaNsisVersion == "4.5.4.0"
			# HACK: 4.4.5 has incorrect version number.
			StrCpy $MinervaNsisVersion "4.4.5.0"
		${EndIf}
		${VersionCompare} "${MINERVA2D_VERSION}" "$MinervaNsisVersion" $R0
		${If} $R0 == 0
			# Same version installed... probably
			${If} $MinervaNsisBitness == ${MINERVA2D_INSTALLER_BITNESS}
				# Very likely the same version
				${IfNot} ${Silent}
					MessageBox MB_OK|MB_ICONINFORMATION "$(MsgMinervaSameVerReinstall)"
				${EndIf}
			${Else}
				# Very likely the same version but different arch
				${IfNot} ${Silent}
!ifdef MINERVA2D_INSTALLER_64
					MessageBox MB_OK|MB_ICONINFORMATION "$(MsgMinerva3264bitSwap)"
!else
					MessageBox MB_OK|MB_ICONEXCLAMATION "$(MsgMinerva3264bitSwap)"
!endif
				${EndIf}
			${EndIf}
		${ElseIf} $R0 == 1
			# Upgrade
			${If} $MinervaNsisBitness == ${MINERVA2D_INSTALLER_BITNESS}
				# Silent about upgrade
			${Else}
				# Upgrade but different arch
				${IfNot} ${Silent}
!ifdef MINERVA2D_INSTALLER_64
					MessageBox MB_OK|MB_ICONINFORMATION "$(MsgMinerva3264bitSwap)"
!else
					MessageBox MB_OK|MB_ICONEXCLAMATION "$(MsgMinerva3264bitSwap)"
!endif
				${EndIf}
			${EndIf}
		${ElseIf} $R0 == 2
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONSTOP "$(MsgMinervaNewerAlreadyInstalled)"
			${EndIf}
			Abort
		${Else}
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONSTOP "Error: Unexpected state"
			${EndIf}
			Abort
		${EndIf}
		!insertmacro SetSectionFlag ${SEC_remove_old_version} ${SF_SELECTED}
		# Detect if Minerva is running...
		${If} ${IsFileinUse} "$MinervaNsisInstallLocation\bin\minerva2d.exe"
			${IfNot} ${Silent}
				MessageBox MB_OK|MB_ICONEXCLAMATION "$(MsgMinervaRunning)"
			${EndIf}
			SetErrorLevel 10
			Abort
		${EndIf}
		pop $R0
	${Else}
		!insertmacro ClearSectionFlag ${SEC_remove_old_version} ${SF_SELECTED}
		SectionSetText ${SEC_remove_old_version} ""
	${EndIf}

	# Detect standalone shell extension
	# TODO: Would it be possible to update Minerva without replacing the standalone shellex?
	ClearErrors
	ReadRegStr $PrevShellExInstallLocation HKLM "Software\Minerva\ShellExtension" "InstallLocation"
	#ReadRegStr $PrevShellExVersion HKLM "Software\Minerva\ShellExtension" "Version"
	ReadRegDWORD $PrevShellExStandalone HKLM "Software\Minerva\ShellExtension" "Standalone"
	#ReadRegStr $PrevShellExMinervaExePath HKLM "Software\Minerva\ShellExtension" "MinervaExePath"
	${If} ${Errors}
		# TODO: Assume no previous version installed or what?
	${EndIf}
	${If} $PrevShellExStandalone == 1
		#!insertmacro SetSectionFlag ${SEC_remove_shellex} ${SF_SELECTED}
	${Else}
		#!insertmacro ClearSectionFlag ${SEC_remove_shellex} ${SF_SELECTED}
		#SectionSetText ${SEC_remove_shellex} ""
	${EndIf}
FunctionEnd

Function un.onInit
	SetShellVarContext all
!ifdef MINERVA2D_INSTALLER_64
	${If} ${RunningX64}
		SetRegView 64
	${Else}
		Abort
	${Endif}
!else
	${If} ${RunningX64}
		SetRegView 64
	${Endif}
!endif

	# Get and use installer language:
	Push $0
	ReadRegStr $0 HKLM "Software\Minerva" "InstallerLanguage"
	${If} $0 != ""
		StrCpy $LANGUAGE $0
	${EndIf}
	Pop $0

	ReadRegDWORD $UninstallShellExStandalone HKLM "Software\Minerva\ShellExtension" "Standalone"
	${If} ${Silent}
		# Only check here if running in silent mode. It's otherwise checked in
		# un.func_UnintallFirstpage_Init in order to display a prompt in the
		# correct language.
		${If} ${IsFileinUse} "$INSTDIR\bin\minerva2d.exe"
			SetErrorLevel 10
			Abort
		${EndIf}
	${EndIf}
FunctionEnd

Function un.func_UnintallFirstpage_Init
	${If} ${IsFileinUse} "$INSTDIR\bin\minerva2d.exe"
		${IfNot} ${Silent}
			MessageBox MB_OK|MB_ICONEXCLAMATION "$(MsgUninstallMinervaRunning)"
		${EndIf}
		SetErrorLevel 10
		Quit
	${EndIf}
FunctionEnd

Function func_ShellExLicensePage_Init
	${IfNot} ${SectionIsSelected} ${SEC_shellex}
		# Skip ShellEx license page if not selected
		Abort
	${EndIf}
FunctionEnd

Var hwndChkDesktopIcon

Function func_DesktopShortcutPage_CheckChange
	${NSD_GetState} $hwndChkDesktopIcon $CreateDesktopIcon
	${If} $CreateDesktopIcon == ${BST_CHECKED}
		StrCpy $CreateDesktopIcon 1
	${Else}
		StrCpy $CreateDesktopIcon 0
	${EndIf}
FunctionEnd

Function func_BeforeInstallPage_Init
	push $R0

	nsDialogs::Create 1018
	pop $R0
	${If} $R0 == error
		Abort
	${EndIf}
	!insertmacro MUI_HEADER_TEXT "$(ConfirmInstallPageHeader)" "$(ConfirmInstallPageDesc)"

	${NSD_CreateLabel} 0u 0u 300u 20u "$(DesktopIconPageDesc2)"
	pop $R0

	${NSD_CreateCheckbox} 0u 20u 300u 10u "$(DesktopIconPageCheckbox)"
	pop $hwndChkDesktopIcon
	${If} $CreateDesktopIcon == 1
		${NSD_Check} $hwndChkDesktopIcon
	${Else}
		${NSD_Uncheck} $hwndChkDesktopIcon
	${EndIf}
	${NSD_OnClick} $hwndChkDesktopIcon func_DesktopShortcutPage_CheckChange

	${NSD_CreateLabel} 0u 40u 300u 140u "$(ConfirmInstallPageDesc2)"
	pop $R0

	# TODO: Add install option summary for review?

	nsDialogs::Show

	pop $R0
FunctionEnd


# Strings
!include "translations\English.nsh"
!include "translations\TradChinese.nsh"
!include "translations\SimpChinese.nsh"
