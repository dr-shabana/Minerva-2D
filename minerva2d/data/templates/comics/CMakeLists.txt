install( FILES 
light_template_comics_empty.png
dark_template_comics_empty.png
DESTINATION
${KDE_INSTALL_DATADIR}/minerva2d/pics
)

install( FILES  
    a4_waffle_grid.m2d   
    BD-EuroTemplate.m2d
    Comics-USTemplate.m2d
    Manga-JpTemplate.m2d
    Tsukirino.m2d
    TsukirinoF.m2d
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/comics/.source)

install( FILES  
    .directory 
    a4_waffle_grid.desktop  
    BD-EuroTemplate.desktop
    Comics-USTemplate.desktop
    Manga-JpTemplate.desktop
    Tsukirino.desktop
    TsukirinoF.desktop
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/comics)
