set(MINERVA2D_ARRANGEDOCKER_SOURCES arrangedocker.cpp arrangedocker_dock.cpp arrange_docker_widget.cpp)
ki18n_wrap_ui(MINERVA2D_ARRANGEDOCKER_SOURCES
    arrange_docker_widget.ui
)

kis_add_library(kritaarrangedocker MODULE ${MINERVA2D_ARRANGEDOCKER_SOURCES})
target_link_libraries(kritaarrangedocker kritaui)
install(TARGETS kritaarrangedocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
