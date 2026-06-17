set(kritakrzexport_SOURCES
    krz_export.cpp
)

kis_add_library(kritakrzexport MODULE ${kritakrzexport_SOURCES})

target_link_libraries(kritakrzexport kritaui kritalibkra kritaimpex)

install(TARGETS kritakrzexport  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

install(FILES minerva2d_krz.desktop DESTINATION ${KDE_INSTALL_APPDIR})
