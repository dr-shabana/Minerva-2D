set(karbon_tools_SOURCES
   KarbonToolsPlugin.cpp
   CalligraphyTool/KarbonCalligraphyTool.cpp
   CalligraphyTool/KarbonCalligraphyOptionWidget.cpp
   CalligraphyTool/KarbonCalligraphyToolFactory.cpp
   CalligraphyTool/KarbonCalligraphicShape.cpp
   CalligraphyTool/KarbonCalligraphicShapeFactory.cpp
   CalligraphyTool/KarbonSimplifyPath.cpp
)

qt_add_resources(karbon_tools_SOURCES karbontools.qrc)

kis_add_library(minerva2d_karbontools MODULE ${karbon_tools_SOURCES})

target_link_libraries(minerva2d_karbontools kritaui kritawidgets KF${KF_MAJOR}::Completion)

install(TARGETS minerva2d_karbontools DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install(FILES  CalligraphyTool/KarbonCalligraphyTool.action DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/actions)

