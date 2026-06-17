set(MINERVA2D_PRESETHISTORY_SOURCES 
    presethistory.cpp 
    presethistory_dock.cpp 
)

kis_add_library(kritapresethistory MODULE ${MINERVA2D_PRESETHISTORY_SOURCES})
target_link_libraries(kritapresethistory kritaui)
install(TARGETS kritapresethistory  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

