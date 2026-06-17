set(kritaexample_SOURCES example.cpp )
kis_add_library(kritaexample MODULE ${kritaexample_SOURCES})
target_link_libraries(kritaexample kritaui)
install(TARGETS kritaexample  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
