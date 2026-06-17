install( FILES 
light_template_animation.png
dark_template_animation.png
DESTINATION
${KDE_INSTALL_DATADIR}/minerva2d/pics
)

install( FILES  
    Anim-Jp-EN.m2d
    Anim-Jp-JP.m2d
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/animation/.source)

install( FILES  
    .directory
    Anim-Jp-EN.desktop 
    Anim-Jp-JP.desktop
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/animation)
