include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../plugin
                    ${CMAKE_CURRENT_BINARY_DIR}/../plugin
                    ${CMAKE_CURRENT_SOURCE_DIR}/../libkis
                    ${CMAKE_CURRENT_BINARY_DIR}/../libkis
)

set(minerva2drunner_SRCS main.cpp)

set(minerva2drunner_PRIVATE_LINK_LIBS
    ${PYTHON_LIBRARY}
    pyminerva2d
    Qt${QT_MAJOR_VERSION}::Core
    Qt${QT_MAJOR_VERSION}::Gui
    Qt${QT_MAJOR_VERSION}::Widgets
    Qt${QT_MAJOR_VERSION}::Xml
    Qt${QT_MAJOR_VERSION}::Network
    Qt${QT_MAJOR_VERSION}::PrintSupport
    Qt${QT_MAJOR_VERSION}::Svg
)

if(WIN32)
    if (NOT QT_MAJOR_VERSION STREQUAL "6")
        configure_file(minerva2drunner.exe.manifest.in ${CMAKE_CURRENT_BINARY_DIR}/minerva2drunner.exe.manifest)
    else()
        configure_file(minerva2drunner6.exe.manifest.in ${CMAKE_CURRENT_BINARY_DIR}/minerva2drunner.exe.manifest)
    endif()
    if (MINGW)
        # CMake does not know how to embed manifest on mingw, so we create our own RC file to be included
        file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/minerva2drunner.exe.manifest.rc "1 24 \"minerva2drunner.exe.manifest\"\n")
        add_library(minerva2drunner_manifest_res OBJECT ${CMAKE_CURRENT_BINARY_DIR}/minerva2drunner.exe.manifest.rc)
        set_property(TARGET minerva2drunner_manifest_res PROPERTY AUTOMOC OFF)
        set_property(TARGET minerva2drunner_manifest_res PROPERTY INCLUDE_DIRECTORIES "")
        set(minerva2drunner_SRCS ${minerva2drunner_SRCS} $<TARGET_OBJECTS:minerva2drunner_manifest_res>)
    else()
        set(minerva2drunner_SRCS ${minerva2drunner_SRCS} 
            ${CMAKE_CURRENT_BINARY_DIR}/minerva2drunner.exe.manifest
        )
    endif()
endif()

add_executable(minerva2drunner ${minerva2drunner_SRCS})
target_include_directories(minerva2drunner SYSTEM PUBLIC "${PYTHON_INCLUDE_DIRS}")
target_link_libraries(minerva2drunner PRIVATE ${minerva2drunner_PRIVATE_LINK_LIBS})

if(APPLE)
    set_target_properties(minerva2drunner PROPERTIES INSTALL_RPATH "@loader_path/../Frameworks;@executable_path/../lib;@executable_path/../Frameworks")
    set_property(TARGET minerva2drunner PROPERTY MACOSX_BUNDLE OFF)
endif()

if (MINGW)
    target_compile_definitions(minerva2drunner PRIVATE _hypot=hypot)
endif (MINGW)

install(TARGETS minerva2drunner ${INSTALL_TARGETS_DEFAULT_ARGS})

if (WIN32)
    add_executable(minerva2drunner_com ${minerva2drunner_SRCS})
    target_include_directories(minerva2drunner_com SYSTEM PUBLIC "${PYTHON_INCLUDE_DIRS}")
    target_link_libraries(minerva2drunner_com PRIVATE ${minerva2drunner_PRIVATE_LINK_LIBS})

    set_target_properties(minerva2drunner_com
        PROPERTIES
            WIN32_EXECUTABLE false
            SUFFIX ".com"
    )
    if (NOT MSVC)
        # MSBuild copies all binaries and library exports into a single 
        # directory. This constitutes a write race condition with minerva2drunner.
        # See https://gitlab.kitware.com/cmake/cmake/-/issues/22133
        set_target_properties(minerva2drunner_com
            PROPERTIES
                OUTPUT_NAME "minerva2drunner"
        )
    endif()

    if (MINGW)
        target_compile_definitions(minerva2drunner_com PRIVATE _hypot=hypot)
    endif (MINGW)

    if (MSVC)
        target_link_options(minerva2drunner_com PRIVATE "/DEBUG:NONE")
    endif()

    install(TARGETS minerva2drunner_com ${INSTALL_TARGETS_DEFAULT_ARGS})
endif (WIN32)
