set(MINERVA2D_TOUCHDOCKER_SOURCES TouchDocker.cpp
    TouchDockerDock.cpp
    TouchDockerWidget.cpp
)

ki18n_wrap_ui(MINERVA2D_TOUCHDOCKER_SOURCES
    TouchDockerWidget.ui
)

kis_add_library(kritatouchdocker MODULE ${MINERVA2D_TOUCHDOCKER_SOURCES})

target_link_libraries(kritatouchdocker kritaui)
install(TARGETS kritatouchdocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
