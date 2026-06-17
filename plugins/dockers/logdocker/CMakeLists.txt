set(MINERVA2D_LOGDOCKER_SOURCES 
    LogDocker.cpp 
    LogDockerDock.cpp
)

ki18n_wrap_ui(MINERVA2D_LOGDOCKER_SOURCES 
    WdgLogDocker.ui
)

kis_add_library(kritalogdocker MODULE ${MINERVA2D_LOGDOCKER_SOURCES})
target_link_libraries(kritalogdocker kritaui)
install(TARGETS kritalogdocker DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
