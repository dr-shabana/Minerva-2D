if (APPLE)
project(kritaintegration)

if (NOT MACOS_UNIVERSAL)
    set(XCODEBUILD_ARCHS "-arch" "${CMAKE_SYSTEM_PROCESSOR}")
endif()

add_custom_target( kritaintegration ALL xcodebuild archive
    -project "${CMAKE_CURRENT_SOURCE_DIR}/integration.xcodeproj" ${XCODEBUILD_ARCHS}
    -target kritaquicklook
    -target kritaspotlight
    -target minerva2d-thumbnailer
    -target minerva2d-preview
    -configuration Release COMMENT build all macOS plugins
)

# TODO kritaquicklook should be removed once 10.x series is unsupported by krita
install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/Build/UninstalledProducts/macosx/minerva2dquicklook.qlgenerator DESTINATION ${KDE_INSTALL_PLUGINDIR})

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/Build/UninstalledProducts/macosx/minerva2dspotlight.mdimporter DESTINATION ${KDE_INSTALL_PLUGINDIR})

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/Build/UninstalledProducts/macosx/minerva2d-thumbnailer.appex DESTINATION ${KDE_INSTALL_PLUGINDIR})

install(DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/Build/UninstalledProducts/macosx/minerva2d-preview.appex DESTINATION ${KDE_INSTALL_PLUGINDIR})
endif(APPLE)
