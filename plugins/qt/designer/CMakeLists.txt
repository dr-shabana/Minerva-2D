find_package(Qt${QT_MAJOR_VERSION} ${MIN_QT_VERSION}
    REQUIRED COMPONENTS
    Designer
)

include_directories(${Qt${QT_MAJOR_VERSION}Designer_INCLUDE_DIRS})

set(MinervaDesignerPlugin_SOURCES
    KisColorSpaceSelectorPlugin.cpp
    MinervaDesignerPluginCollection.cpp
)

kis_add_library(kritadesignerplugin MODULE ${MinervaDesignerPlugin_SOURCES})

target_link_libraries(kritadesignerplugin kritaui)
