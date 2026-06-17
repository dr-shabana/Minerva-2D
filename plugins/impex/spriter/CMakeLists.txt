# export

set(kritaspriterexport_SOURCES
    kis_spriter_export.cpp
)

kis_add_library(kritaspriterexport MODULE ${kritaspriterexport_SOURCES})

target_link_libraries(kritaspriterexport kritaui kritaimpex)

install(TARGETS kritaspriterexport  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

install(FILES minerva2d_spriter.desktop DESTINATION ${KDE_INSTALL_APPDIR})
