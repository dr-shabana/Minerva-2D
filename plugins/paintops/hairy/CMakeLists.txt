set(kritahairypaintop_SOURCES
    hairy_paintop_plugin.cpp
    kis_hairy_paintop.cpp
    kis_hairy_paintop_settings.cpp
    kis_hairy_paintop_settings_widget.cpp
    bristle.cpp
    hairy_brush.cpp
    trajectory.cpp
    KisHairyBristleOptionData.cpp
    KisHairyBristleOptionModel.cpp
    KisHairyBristleOptionWidget.cpp
    KisHairyInkOptionData.cpp
    KisHairyInkOptionModel.cpp
    KisHairyInkOptionWidget.cpp
    )

ki18n_wrap_ui(kritahairypaintop_SOURCES wdgInkOptions.ui  wdghairyshapeoptions.ui wdgbristleoptions.ui)

kis_add_library(kritahairypaintop MODULE ${kritahairypaintop_SOURCES})

target_link_libraries(kritahairypaintop kritalibpaintop)

install(TARGETS kritahairypaintop  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install( FILES
    minerva2d-sumi.png DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/images)


