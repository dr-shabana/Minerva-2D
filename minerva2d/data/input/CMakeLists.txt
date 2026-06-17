install(FILES
    clipstudiopaintcompatible.profile
    minerva2ddefault.profile
    painttoolsaicompatible.profile
    photoshopcompatible.profile
    DESTINATION  ${KDE_INSTALL_DATADIR}/minerva2d/input
)
if (WIN32)
   install(FILES
        tabletpro.profile
        DESTINATION  ${KDE_INSTALL_DATADIR}/minerva2d/input
    )
endif()

