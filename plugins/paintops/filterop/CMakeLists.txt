set(kritafilterop_SOURCES
    filterop.cpp
    kis_filterop.cpp
    kis_filterop_settings.cpp
    kis_filterop_settings_widget.cpp
    )


kis_add_library(kritafilterop MODULE ${kritafilterop_SOURCES})

target_link_libraries(kritafilterop kritalibpaintop)

install(TARGETS kritafilterop  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install( FILES
    minerva2d-filterop.png
    DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/images)
