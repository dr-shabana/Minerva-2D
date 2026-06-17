set(MINERVA2D_COMPOSITIONDOCKER_SOURCES compositionmodel.cpp compositiondocker.cpp compositiondocker_dock.cpp )

ki18n_wrap_ui(MINERVA2D_COMPOSITIONDOCKER_SOURCES
    wdgcompositiondocker.ui
)

kis_add_library(kritacompositiondocker MODULE ${MINERVA2D_COMPOSITIONDOCKER_SOURCES})
target_link_libraries(kritacompositiondocker kritaui)
install(TARGETS kritacompositiondocker DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
