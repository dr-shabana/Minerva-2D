# generate minerva2dversion.h
configure_file(minerva2dversion.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/minerva2dversion.h)

# generate kritagitversion.h
configure_file(kritagitversion.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/minerva2dgitversion.h)

set(minerva2dversion_LIB_SRCS
    MinervaVersionWrapper.cpp
)

kis_add_library(minerva2dversion SHARED ${minerva2dversion_LIB_SRCS})
target_link_libraries(minerva2dversion Qt${QT_MAJOR_VERSION}::Core)
generate_export_header(minerva2dversion BASE_NAME minerva2dversion)

set_target_properties(minerva2dversion PROPERTIES
    VERSION ${GENERIC_MINERVA2D_LIB_VERSION} SOVERSION ${GENERIC_MINERVA2D_LIB_SOVERSION}
)
install(TARGETS minerva2dversion ${INSTALL_TARGETS_DEFAULT_ARGS} )

