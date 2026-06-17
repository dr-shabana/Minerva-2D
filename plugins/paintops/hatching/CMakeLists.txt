set(kritahatchingpaintop_SOURCES
    hatching_paintop_plugin.cpp
    kis_hatching_paintop.cpp
    kis_hatching_paintop_settings.cpp
    kis_hatching_paintop_settings_widget.cpp
    hatching_brush.cpp
    KisHatchingOptionsData.cpp
    KisHatchingOptionsModel.cpp
    KisHatchingOptionsWidget.cpp
    KisHatchingPreferencesData.cpp
    KisHatchingPreferencesModel.cpp
    KisHatchingPreferencesWidget.cpp
    )

ki18n_wrap_ui(kritahatchingpaintop_SOURCES wdghatchingpreferences.ui wdghatchingoptions.ui)

kis_add_library(kritahatchingpaintop MODULE ${kritahatchingpaintop_SOURCES})

target_link_libraries(kritahatchingpaintop kritalibpaintop)

install(TARGETS kritahatchingpaintop  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install( FILES  minerva2d-hatching.png DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/images)

