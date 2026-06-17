set (minerva2d_BUNDLE_FILES
     README
     Minerva_4_Default_Resources.bundle
     Minerva_Artists_SeExpr_examples.bundle
     RGBA_brushes.bundle
)

if (NOT ANDROID)
    set (minerva2d_BUNDLE_FILES
         ${minerva2d_BUNDLE_FILES}
         Minerva_3_Default_Resources.bundle
         )
endif()

install( FILES
    ${minerva2d_BUNDLE_FILES}
    DESTINATION  ${KDE_INSTALL_DATADIR}/minerva2d/bundles)
