set(MINERVA2D_OVERVIEWDOCKER_SOURCES overviewdocker.cpp
    overviewdocker_dock.cpp
    overviewwidget.cc
    overviewdocker_page.cpp)
kis_add_library(kritaoverviewdocker MODULE ${MINERVA2D_OVERVIEWDOCKER_SOURCES})
target_link_libraries(kritaoverviewdocker kritaui)
install(TARGETS kritaoverviewdocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
