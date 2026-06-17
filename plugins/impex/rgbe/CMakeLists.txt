add_subdirectory(tests)

add_library(kritargbeimportutils STATIC RGBEImportUtils.cpp)
target_link_libraries(kritargbeimportutils PUBLIC kritaimage)

set(kritargbeimport_SOURCES
    RGBEImport.cpp
)

add_library(kritargbeimport MODULE ${kritargbeimport_SOURCES})
target_link_libraries(kritargbeimport kritaui kritargbeimportutils)

install(TARGETS kritargbeimport DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

set(kritargbeexport_SOURCES
    RGBEExport.cpp
    kis_wdg_options_rgbe.cpp
)

ki18n_wrap_ui(kritargbeexport_SOURCES kis_wdg_options_rgbe.ui )

kis_add_library(kritargbeexport MODULE ${kritargbeexport_SOURCES})

target_link_libraries(kritargbeexport kritaui kritalibkra kritaimpex)

install(TARGETS kritargbeexport  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

install(FILES minerva2d_rgbe.desktop DESTINATION ${KDE_INSTALL_APPDIR})
