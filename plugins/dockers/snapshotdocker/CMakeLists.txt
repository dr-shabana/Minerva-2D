set(kritasnapshotdocker_SOURCES
  KisSnapshotModel.cpp
  SnapshotDocker.cpp
  SnapshotPlugin.cpp
  KisSnapshotView.cpp
  )

kis_add_library(kritasnapshotdocker MODULE ${kritasnapshotdocker_SOURCES})
target_link_libraries(kritasnapshotdocker kritaimage kritaui)
install(TARGETS kritasnapshotdocker DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
