project( kritaplatformpluginxcb )

set ( kritaplatformpluginxcb_SRCS
    MinervaPlatformPluginXcb.cpp
    KisExtendedModifiersMapperX11.cpp
)

kis_add_library(kritaplatformpluginxcb MODULE ${kritaplatformpluginxcb_SRCS})

target_link_libraries(kritaplatformpluginxcb PRIVATE kritaglobal kritaui)

if (QT_MAJOR_VERSION STREQUAL "5")
    target_link_libraries(kritaplatformpluginxcb PRIVATE Qt${QT_MAJOR_VERSION}::X11Extras)
endif()

target_link_libraries(kritaplatformpluginxcb PRIVATE ${X11_X11_LIB})

install(TARGETS kritaplatformpluginxcb DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

