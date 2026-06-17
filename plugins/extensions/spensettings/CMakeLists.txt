set(kritaspensettings_SOURCES
    SPenSettings.cpp
    KisSPenSettings.cpp
    )

ki18n_wrap_ui(kritaspensettings_SOURCES
    wdg_spensettings.ui
    )

qt_add_resources(kritaspensettings_SOURCES
    spensettings.qrc
)

kis_add_library(kritaspensettings MODULE ${kritaspensettings_SOURCES})
target_link_libraries(kritaspensettings kritaui)
install(TARGETS kritaspensettings  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

install( FILES  SPenSettings.action  DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/actions)

install( FILES  spen-remote.svg
                DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pics)

