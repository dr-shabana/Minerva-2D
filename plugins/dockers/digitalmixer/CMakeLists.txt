set(MINERVA2D_DIGITALMIXER_SOURCES digitalmixer.cc digitalmixer_dock.cc )
kis_add_library(kritadigitalmixer MODULE ${MINERVA2D_DIGITALMIXER_SOURCES})
target_link_libraries(kritadigitalmixer kritaui)
install(TARGETS kritadigitalmixer  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
