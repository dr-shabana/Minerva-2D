install( FILES 
light_template_DIN_A3_landscape.png
dark_template_DIN_A3_landscape.png
light_template_DIN_A4_portrait.png
dark_template_DIN_A4_portrait.png
light_template_ratio_1610.png
dark_template_ratio_1610.png
light_template_ratio_2391.png
dark_template_ratio_2391.png
light_template_ratio_43.png
dark_template_ratio_43.png
light_template_web_design.png
dark_template_web_design.png
DESTINATION
${KDE_INSTALL_DATADIR}/minerva2d/pics)

install( FILES  
    Designcinema16_10_2484x1200_96dpiRGB_8bit_.m2d
    Designcinema2.39_1_2484x1040_96dpiRGB_8bit_.m2d
    DesignpresentationA3Landscape_4960x3508_300dpiRGB_8bit_.m2d
    DesignpresentationA4portrait_2480x3508_300dpiRGB_8bit_.m2d
    Designscreen4_3_2250x1680_96dpiRGB_8bit_.m2d
    web_design.m2d
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/design/.source)

install( FILES  
    .directory 
    Designcinema16_10_2484x1200_96dpiRGB_8bit_.desktop
    Designcinema2.39_1_2484x1040_96dpiRGB_8bit_.desktop
    DesignpresentationA3Landscape_4960x3508_300dpiRGB_8bit_.desktop
    DesignpresentationA4portrait_2480x3508_300dpiRGB_8bit_.desktop
    Designscreen4_3_2250x1680_96dpiRGB_8bit_.desktop
    web_design.desktop
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/design)
