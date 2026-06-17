set(MINERVA2D_PRESETDOCKER_SOURCES presetdocker.cpp presetdocker_dock.cpp )
kis_add_library(kritapresetdocker MODULE ${MINERVA2D_PRESETDOCKER_SOURCES})
target_link_libraries(kritapresetdocker kritaui)
install(TARGETS kritapresetdocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
