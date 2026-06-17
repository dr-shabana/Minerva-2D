set(MINERVA2D_CHANNELDOCKER_SOURCES
    channelmodel.cpp
    channeldocker.cpp
    channeldocker_dock.cpp
    ChannelDockerWidget.cpp
    KisChannelsThumbnailsStrokeStrategy.cpp
)
kis_add_library(kritachanneldocker MODULE ${MINERVA2D_CHANNELDOCKER_SOURCES})
target_link_libraries(kritachanneldocker kritaui)
install(TARGETS kritachanneldocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
