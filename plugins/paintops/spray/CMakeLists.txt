set(kritaspraypaintop_SOURCES
    spray_paintop_plugin.cpp
    kis_spray_paintop.cpp
    kis_spray_paintop_settings.cpp
    kis_spray_paintop_settings_widget.cpp
    spray_brush.cpp
    KisSprayRandomDistributions.cpp
    KisSprayOpOptionData.cpp
    KisSprayOpOptionModel.cpp
    KisSprayOpOptionWidget.cpp
    KisSprayOpOption.cpp
    
    KisSprayShapeOptionData.cpp
    KisSprayShapeOptionModel.cpp
    KisSprayShapeOptionWidget.cpp
    
    KisSprayShapeDynamicsOptionData.cpp
    KisSprayShapeDynamicsOptionModel.cpp
    KisSprayShapeDynamicsOptionWidget.cpp
    
    )

ki18n_wrap_ui(kritaspraypaintop_SOURCES wdgsprayoptions.ui wdgsprayshapeoptions.ui wdgshapedynamicsoptions.ui )

kis_add_library(kritaspraypaintop MODULE ${kritaspraypaintop_SOURCES})

target_link_libraries(kritaspraypaintop kritalibpaintop)

install(TARGETS kritaspraypaintop  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})


########### install files ###############

install( FILES
    minerva2d-spray.png DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/images)

