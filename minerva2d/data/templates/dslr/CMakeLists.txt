install( FILES 
light_template_dslr.png
dark_template_dslr.png
DESTINATION
${KDE_INSTALL_DATADIR}/minerva2d/pics )

install( FILES  
    Canon_550D_5184x3456.m2d
    Canon_5Dmk3_5760x3840.m2d
    Nikon_D3000_3872x2592.m2d
    Nikon_D5000_4288x2848.m2d
    Nikon_D7000_4928x3264.m2d
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/dslr/.source)

install( FILES  
    .directory
    Canon_550D_5184x3456.desktop
    Canon_5Dmk3_5760x3840.desktop
    Nikon_D3000_3872x2592.desktop
    Nikon_D5000_4288x2848.desktop
    Nikon_D7000_4928x3264.desktop
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/dslr)
