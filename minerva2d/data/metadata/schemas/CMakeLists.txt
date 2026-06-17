########### install schemas #############
install( FILES
    dc.schema
    exif.schema
    tiff.schema
    mkn.schema
    xmp.schema
    xmpmm.schema
    xmprights.schema

    DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/metadata/schemas)
                                                             
