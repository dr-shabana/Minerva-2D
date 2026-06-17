# NOTE Disable trivial Qt keywords due conflicts w/ some Python.h header
# (at least version 3.3 of it has a member PyType_Spec::slots)
add_definitions(-DQT_NO_KEYWORDS)
configure_file(config.h.cmake ${CMAKE_CURRENT_BINARY_DIR}/config.h)

set(SOURCES
    utilities.cpp
    Pyminerva2dModule.cpp
    PythonPluginManager.cpp
    PythonPluginsModel.cpp
)

ki18n_wrap_ui(SOURCES
    info.ui
    manager.ui
)

kis_add_library(pyminerva2d STATIC ${SOURCES})

target_include_directories(pyminerva2d SYSTEM PUBLIC "${PYTHON_INCLUDE_DIRS}")

target_link_libraries(
    pyminerva2d
    ${PYTHON_LIBRARY}
    kritaui
    kritalibkis
  )

if (QT_MAJOR_VERSION STREQUAL "6")
    target_link_libraries(pyminerva2d KF6::ColorScheme)
endif()

kis_add_library(kritapyminerva2d MODULE
    plugin.cpp
    pyqtpluginsettings.cpp
  )

target_link_libraries(
    kritapyminerva2d
    pyminerva2d
  )

if (MINGW)
    target_compile_definitions(pyminerva2d PRIVATE _hypot=hypot)
endif()
if (WIN32)
    # Banish Python 3.8 from mucking up Boost.Assert use of snprintf.
    # https://github.com/boostorg/system/issues/32
    target_compile_definitions(pyminerva2d PRIVATE HAVE_SNPRINTF=1)
endif (WIN32)

install(TARGETS kritapyminerva2d DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

# Install "built-in" api
install(
    DIRECTORY krita
    DESTINATION ${KDE_INSTALL_LIBDIR}/minerva2d-python-libs
    FILES_MATCHING PATTERN "*.py"
)

