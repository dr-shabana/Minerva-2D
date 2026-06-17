set(MINERVA2D_SPECIFICCOLORSELECTOR_SOURCES 
    specificcolorselector.cc 
    specificcolorselector_dock.cc 
    kis_specific_color_selector_widget.cc 
)

ki18n_wrap_ui(MINERVA2D_SPECIFICCOLORSELECTOR_SOURCES
    wdgSpecificColorSelectorWidget.ui
)


kis_add_library(kritaspecificcolorselector MODULE ${MINERVA2D_SPECIFICCOLORSELECTOR_SOURCES})
target_link_libraries(kritaspecificcolorselector kritaui ${LINK_OPENEXR_LIB})
install(TARGETS kritaspecificcolorselector  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
