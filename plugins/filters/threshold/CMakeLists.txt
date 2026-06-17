set(kritathreshold_SOURCES threshold.cpp )

ki18n_wrap_ui(kritathreshold_SOURCES
    wdg_threshold.ui
    )

kis_add_library(kritathreshold MODULE ${kritathreshold_SOURCES})
target_link_libraries(kritathreshold kritaui)
install(TARGETS kritathreshold  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install( FILES
    threshold.action
DESTINATION  ${KDE_INSTALL_DATADIR}/minerva2d/actions)

