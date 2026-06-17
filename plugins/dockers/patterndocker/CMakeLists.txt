set(MINERVA2D_PATTERNDOCKER_SOURCES patterndocker.cpp patterndocker_dock.cpp )
kis_add_library(kritapatterndocker MODULE ${MINERVA2D_PATTERNDOCKER_SOURCES})
target_link_libraries(kritapatterndocker kritaui)
install(TARGETS kritapatterndocker  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
