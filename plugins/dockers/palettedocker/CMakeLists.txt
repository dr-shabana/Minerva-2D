set(MINERVA2D_PALETTEDOCKER_SOURCES
    palettedocker.cpp palettedocker_dock.cpp
    )

ki18n_wrap_ui(MINERVA2D_PALETTEDOCKER_SOURCES
    wdgpalettedock.ui
)

kis_add_library(kritapalettedocker MODULE ${MINERVA2D_PALETTEDOCKER_SOURCES})
target_link_libraries(kritapalettedocker kritaui)
install(TARGETS kritapalettedocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
