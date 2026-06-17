########### install files ###############

if (FOUNDATION_BUILD)
    install(FILES
        BreezeDark.colors
        BreezeHighContrast.colors
        BreezeLight.colors
         ${schemefiles} DESTINATION ${KDE_INSTALL_DATADIR}/color-schemes
)
endif()

install(FILES
MinervaNeutral.colors
MinervaBlender.colors
MinervaBright.colors
MinervaDark.colors
MinervaDarkOrange.colors
MinervaDarker.colors
 ${schemefiles} DESTINATION ${KDE_INSTALL_DATADIR}/color-schemes
)

