add_subdirectory(tests)

set(kritaqmlexport_SOURCES
    qml_converter.cc
    qml_export.cc
    )

kis_add_library(kritaqmlexport MODULE ${kritaqmlexport_SOURCES})

target_link_libraries(kritaqmlexport kritaui kritaimpex)

install(TARGETS kritaqmlexport  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
