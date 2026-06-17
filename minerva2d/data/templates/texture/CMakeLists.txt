install( FILES 
light_template_texture.png
dark_template_texture.png
DESTINATION
${KDE_INSTALL_DATADIR}/minerva2d/pics )
install( FILES  

Texture1024x10248bitsrgb.m2d
Texture1k32bitscalar.m2d
Texture1k8bitsrgb.m2d
Texture2048x20488bitsrgb.m2d
Texture256x2568bitsrgb.m2d
Texture2k32bitscalar.m2d
Texture2k8bitsrgb.m2d
Texture4096x40968bitsrgb.m2d
Texture4k32bitscalar.m2d
Texture4k8bitsrgb.m2d
Texture512x5128bitsrgb.m2d
Texture8k32bitscalar.m2d
Texture8k8bitsrgb.m2d
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/texture/.source)

install( FILES  
    .directory

Texture1024x10248bitsrgb.desktop
Texture1k32bitscalar.desktop
Texture1k8bitsrgb.desktop
Texture2048x20488bitsrgb.desktop
Texture256x2568bitsrgb.desktop
Texture2k32bitscalar.desktop
Texture2k8bitsrgb.desktop
Texture4096x40968bitsrgb.desktop
Texture4k32bitscalar.desktop
Texture4k8bitsrgb.desktop
Texture512x5128bitsrgb.desktop
Texture8k32bitscalar.desktop
Texture8k8bitsrgb.desktop
DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/templates/texture)
