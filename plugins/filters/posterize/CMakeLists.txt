set(kritaposterize_SOURCES posterize.cpp )
kis_add_library(kritaposterize MODULE ${kritaposterize_SOURCES})
target_link_libraries(kritaposterize kritaui)
install(TARGETS kritaposterize  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
