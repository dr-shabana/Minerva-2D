set(MINERVA2D_TASKSETDOCKER_SOURCES tasksetmodel.cpp tasksetdocker.cpp tasksetdocker_dock.cpp taskset_resource.cpp)

ki18n_wrap_ui(MINERVA2D_TASKSETDOCKER_SOURCES
    wdgtasksetdocker.ui
)
kis_add_library(kritatasksetdocker MODULE ${MINERVA2D_TASKSETDOCKER_SOURCES})
target_link_libraries(kritatasksetdocker kritaui)
install(TARGETS kritatasksetdocker DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
