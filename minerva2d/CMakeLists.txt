add_subdirectory( dtd )
add_subdirectory( data )
add_subdirectory( integration )
# Install the application icons following the freedesktop icon theme spec
add_subdirectory( "pics/branding/${BRANDING}" )

if (ANDROID)
    if (QT_MAJOR_VERSION STREQUAL "5")
        set (QtAndroidExtras_INCLUDE_DIRS ${Qt5AndroidExtras_INCLUDE_DIRS})
        include_directories (${QtAndroidExtras_INCLUDE_DIRS})
    endif()
endif()

set(minerva2d_SRCS main.cc)

# Set the application icon on the application
if (NOT APPLE)
	file(GLOB ICON_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/*-apps-minerva2d.png")
else()
    # XCode below 26 cannot work with .icon format
    if(${XCODE_VERSION} VERSION_GREATER_EQUAL "26.0")
        find_program(XCRUN_EXECUTABLE NAMES xcrun)
        set(MINERVA2D_ASSETS_ICON "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/minerva2d.icon")
        cmake_path(SET ASSETS_PATH "${CMAKE_CURRENT_BINARY_DIR}/assets")

        set(ASSETS_FILES "${ASSETS_PATH}/Assets.car" "${ASSETS_PATH}/minerva2d.icns")
        add_custom_command(
          OUTPUT ${ASSETS_FILES}
          COMMAND ${CMAKE_COMMAND} ARGS -E make_directory "${ASSETS_PATH}"
          COMMAND ${XCRUN_EXECUTABLE} ARGS actool "${MINERVA2D_ASSETS_ICON}"
            --compile ${ASSETS_PATH}
            --platform macosx --minimum-deployment-target ${MACOS_MINIMUM_VERSION}
            --app-icon krita --output-partial-info-plist "${CMAKE_CURRENT_BINARY_DIR}/minerva2d_icon.plist"
            --output-format human-readable-text
            --standalone-icon-behavior all
          DEPENDS
            "${MINERVA2D_ASSETS_ICON}"
          WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
        )
    else()
        set(ICON_SRCS
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/16-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/32-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/48-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/128-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/256-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/512-apps-minerva2d.png"
             "${CMAKE_CURRENT_SOURCE_DIR}/pics/branding/${BRANDING}/1024-apps-minerva2d.png"
        )
    endif() # XCode version
endif()

if (WIN32)
    # Private headers are needed for main.cc to enable WinTab support
    set_source_files_properties(
        main.cc
        PROPERTIES
        INCLUDE_DIRECTORIES "${Qt${QT_MAJOR_VERSION}Gui_PRIVATE_INCLUDE_DIRS}"
        )
endif()

if (WIN32)
    set(minerva2d_windows_stub_ICONS_SRCS "")
    ecm_add_app_icon(minerva2d_windows_stub_ICONS_SRCS ICONS ${ICON_SRCS} OUTFILE_BASENAME krita)

    # This is used to generate an ICO file for the file icon, We don't actually
    # want to embed this icon into an EXE.
	file(GLOB krafile_ICON_SRCS "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/*-mimetypes-application-x-minerva2d.png")
    set(krafile_dummy_ICONS_SRCS "")
    ecm_add_app_icon(krafile_dummy_ICONS_SRCS ICONS ${krafile_ICON_SRCS} OUTFILE_BASENAME kritafile)
    add_library(krafile_dummy_obj OBJECT ${krafile_dummy_ICONS_SRCS})

    # These icons are used to replace those in the shell extension package.
    install(
        FILES
            ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.ico
            ${CMAKE_CURRENT_BINARY_DIR}/minerva2dfile.ico
        DESTINATION ${CMAKE_INSTALL_PREFIX}/installer
    )
elseif(APPLE)
    if(${XCODE_VERSION} VERSION_GREATER_EQUAL "26.0")
      set_source_files_properties(${ASSETS_FILES} PROPERTIES MACOSX_PACKAGE_LOCATION Resources)
    else()
      ecm_add_app_icon(minerva2d_SRCS OUTFILE_BASENAME krita ICONS ${ICON_SRCS})
    endif()
else()
    ecm_add_app_icon(minerva2d_SRCS ICONS ${ICON_SRCS})
endif()

# Install the mimetype icons
ecm_install_icons(ICONS
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/16-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/22-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/32-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/48-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/64-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/128-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/256-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/512-mimetypes-application-x-minerva2d.png"
    "${CMAKE_CURRENT_SOURCE_DIR}/pics/mimetypes/1024-mimetypes-application-x-minerva2d.png"
    DESTINATION ${KDE_INSTALL_ICONDIR} THEME hicolor)

# separate listing, both used by Minerva and MinervaSketch
set(minerva2d_QRCS
    ${CMAKE_SOURCE_DIR}/minerva2d/minerva2d.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/Breeze-dark/breeze-dark-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/Breeze-light/breeze-light-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/layerbox/layerbox-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/layers/layers-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/misc-light/misc-light-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/misc-dark/misc-dark-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/paintops/paintops-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/tools/SVG/16/tools-svg-16-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/tool_transform/tool-transform-icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/svg/svg-icons.qrc
    ${CMAKE_SOURCE_DIR}/libs/flake/flake.qrc
    ${CMAKE_SOURCE_DIR}/libs/widgets/minerva2dwidgets.qrc
    ${CMAKE_SOURCE_DIR}/pics/icons.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/data/aboutdata/aboutdata.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/data/shaders/shaders.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/data/cursors/cursors.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/data/gamutmasks/gamutmasks.qrc
    ${CMAKE_SOURCE_DIR}/plugins/paintops/defaultpresets/defaultpresets.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/branding/${BRANDING}/branding.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/data/splash/splash.qrc
    ${CMAKE_SOURCE_DIR}/minerva2d/pics/sponsors/sponsors.qrc
    CACHE INTERNAL "minerva2d_QRCS"
)

if (QT_MAJOR_VERSION STREQUAL "6")
    list(APPEND minerva2d_QRCS ${CMAKE_SOURCE_DIR}/minerva2d/data/mime-database/mime-database.qrc)
endif()

qt_add_resources(minerva2d_SRCS ${minerva2d_QRCS})

if (ANDROID AND QT_MAJOR_VERSION STREQUAL "5")
    kis_add_library(krita SHARED ${minerva2d_SRCS})
    target_link_libraries(krita PRIVATE Qt5::AndroidExtras)
elseif (WIN32)
    # Build the main implementation into a DLL to be called by a stub EXE.
    kis_add_library(krita SHARED ${minerva2d_SRCS})
    set_target_properties(krita PROPERTIES PREFIX "")
else()
    add_executable(krita ${minerva2d_SRCS})
endif()
target_link_libraries(krita
    PRIVATE
                      kritamultiarch
                      kritaui
                      Qt${QT_MAJOR_VERSION}::Core
                      Qt${QT_MAJOR_VERSION}::Gui
                      Qt${QT_MAJOR_VERSION}::Widgets
                      Qt${QT_MAJOR_VERSION}::Xml
                      Qt${QT_MAJOR_VERSION}::Network
                      Qt${QT_MAJOR_VERSION}::PrintSupport
                      Qt${QT_MAJOR_VERSION}::Svg)
if(HAVE_KCRASH)
    target_link_libraries(krita PRIVATE KF${KF_MAJOR}::Crash)
endif()

if (APPLE)
    set(MINERVA2D_VERSION_NUMBER_STRING "${MINERVA2D_STABLE_VERSION_MAJOR}.${MINERVA2D_STABLE_VERSION_MINOR}.${MINERVA2D_VERSION_RELEASE}")
    set_target_properties(krita PROPERTIES INSTALL_RPATH "@loader_path/../../../../lib;@loader_path/../lib;
        @loader_path/../Frameworks;@executable_path/../../../../lib;@executable_path/../lib;@executable_path/../Frameworks")
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_INFO_PLIST ${CMAKE_CURRENT_SOURCE_DIR}/Info.plist.template)
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_GUI_IDENTIFIER "org.krita")
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_BUNDLE_NAME "Minerva")
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_ICON_FILE "krita")
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_LONG_VERSION_STRING ${MINERVA2D_VERSION_STRING})
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_SHORT_VERSION_STRING ${MINERVA2D_VERSION_NUMBER_STRING})
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_BUNDLE_VERSION ${MINERVA2D_VERSION_NUMBER_STRING})
    set_target_properties(krita PROPERTIES MACOSX_BUNDLE_COPYRIGHT "GNU Public License, V2 or, at your option, any later version.")
endif ()

if (NOT ANDROID)
  set(KRITAVERSION_SRCS minerva2dversion.cpp)
  add_executable(minerva2d_version ${KRITAVERSION_SRCS})
  target_link_libraries(minerva2d_version
    PRIVATE
        Qt${QT_MAJOR_VERSION}::Core
        minerva2dversion
  )

  if(APPLE)
      set_target_properties(minerva2d_version PROPERTIES INSTALL_RPATH "@loader_path/../Frameworks;@executable_path/../lib;@executable_path/../Frameworks")
      set_property(TARGET minerva2d_version PROPERTY MACOSX_BUNDLE OFF)
  endif ()

  install(TARGETS minerva2d_version ${INSTALL_TARGETS_DEFAULT_ARGS})
endif()


if(APPLE)
    set(MINERVA2D_ASSET_KRZ_ICNS "minerva2d-krz.icns" "minerva2d-kra.icns")
    add_custom_command(
      OUTPUT ${MINERVA2D_ASSET_KRZ_ICNS}
      COMMAND ${CMAKE_COMMAND}
      ARGS -E copy
      "./pics/mimetypes/krz/minerva2d-krz.icns"
      "./pics/mimetypes/minerva2d-kra.icns"
      "${CMAKE_CURRENT_BINARY_DIR}"
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    )
    set_source_files_properties(${MINERVA2D_ASSET_KRZ_ICNS} PROPERTIES MACOSX_PACKAGE_LOCATION Resources)

    # make krita depend on assets icons
    if(${XCODE_VERSION} VERSION_GREATER_EQUAL "26.0")
      target_sources(krita PRIVATE ${ASSETS_FILES})
    endif()
    target_sources(krita PRIVATE ${MINERVA2D_ASSET_KRZ_ICNS})

    install(TARGETS krita ${INSTALL_TARGETS_DEFAULT_ARGS} BUNDLE DESTINATION bin)
else()
    install(TARGETS krita ${INSTALL_TARGETS_DEFAULT_ARGS})
endif()
install(FILES org.kde.minerva2d.desktop DESTINATION ${KDE_INSTALL_APPDIR})
install(FILES  minerva2d.action minerva2dmenu.action DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/actions)
install(FILES  org.kde.minerva2d.appdata.xml DESTINATION ${KDE_INSTALL_METAINFODIR} )

install(DIRECTORY DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/shortcuts)

if (WIN32)
    configure_file(versioninfo.rc.in ${CMAKE_CURRENT_BINARY_DIR}/versioninfo.rc)
    if (QT_MAJOR_VERSION STREQUAL "6")
        configure_file(minerva2d6.exe.manifest.in ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.exe.manifest)
    else()
        configure_file(minerva2d.exe.manifest.in ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.exe.manifest)
    endif()
    if (MINGW)
        # CMake does not know how to embed manifest on mingw, so we create our own RC file to be included
        file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.exe.manifest.rc "1 24 \"minerva2d.exe.manifest\"\n")
        set(MINERVA2D_MANIFEST_SRC ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.exe.manifest.rc)
    else()
        set(MINERVA2D_MANIFEST_SRC
            ${CMAKE_CURRENT_BINARY_DIR}/minerva2d.exe.manifest)
    endif()
    add_executable(minerva2d_windows_stub_exe
        windows_stub_main.cpp
        ${minerva2d_windows_stub_ICONS_SRCS}
        ${CMAKE_CURRENT_BINARY_DIR}/versioninfo.rc
        ${MINERVA2D_MANIFEST_SRC}
    )
    target_link_libraries(minerva2d_windows_stub_exe PRIVATE krita)
    if (QT_MAJOR_VERSION STREQUAL "6")
        target_link_libraries(minerva2d_windows_stub_exe PRIVATE Qt6::EntryPointPrivate)
    else()
        target_link_libraries(minerva2d_windows_stub_exe PRIVATE Qt5::WinMain)
    endif()
    set_target_properties(minerva2d_windows_stub_exe
        PROPERTIES
            OUTPUT_NAME "krita"
    )
    if (MSVC)
        target_link_options(minerva2d_windows_stub_exe PRIVATE "/DEBUG:NONE")
    endif()
    install(TARGETS minerva2d_windows_stub_exe ${INSTALL_TARGETS_DEFAULT_ARGS})

    add_executable(minerva2d_windows_stub_com
        windows_stub_main.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/versioninfo.rc
        ${MINERVA2D_MANIFEST_SRC}
    )
    target_link_libraries(minerva2d_windows_stub_com PRIVATE krita)
    set_target_properties(minerva2d_windows_stub_com
        PROPERTIES
            WIN32_EXECUTABLE false
            OUTPUT_NAME "krita"
            SUFFIX ".com"
    )
    if (MSVC)
        target_link_options(minerva2d_windows_stub_com PRIVATE "/DEBUG:NONE")
        # If MSVC uses incremental linking, it will race the database
        # for minerva2d.exe with the one for minerva2d.com.
        add_dependencies(minerva2d_windows_stub_com minerva2d_windows_stub_exe)
    endif()
    install(TARGETS minerva2d_windows_stub_com ${INSTALL_TARGETS_DEFAULT_ARGS})
endif (WIN32)
