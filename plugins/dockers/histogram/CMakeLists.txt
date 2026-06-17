set(MINERVA2D_HISTOGRAMDOCKER_SOURCES
    histogramdocker.cpp
    histogramdocker_dock.cpp
    histogramdockerwidget.cpp
    HistogramComputationStrokeStrategy.cpp)

kis_add_library(kritahistogramdocker MODULE ${MINERVA2D_HISTOGRAMDOCKER_SOURCES})
target_link_libraries(kritahistogramdocker kritaui)
install(TARGETS kritahistogramdocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
