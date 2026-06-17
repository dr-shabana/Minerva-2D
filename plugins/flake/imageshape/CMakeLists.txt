project(imageshape)

set ( ImageShape_SRCS
    ImageShapePlugin.cpp
    ImageShape.cpp
    ImageShapeFactory.cpp
)

kis_add_library(minerva2d_shape_image MODULE ${ImageShape_SRCS})

target_link_libraries(minerva2d_shape_image kritaflake kritawidgets KF${KF_MAJOR}::I18n )

install(TARGETS minerva2d_shape_image DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

