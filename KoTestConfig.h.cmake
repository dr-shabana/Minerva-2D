#include <KoConfig.h>

/* This variable contains the path to the root of the source directory */
#define MINERVA2D_SOURCE_DIR "${CMAKE_SOURCE_DIR}"

/* This variable contains the path to the data install dir */
#define MINERVA2D_RESOURCE_DIRS_FOR_TESTS "${CMAKE_INSTALL_PREFIX}/${KDE_INSTALL_DATADIR};${CMAKE_SOURCE_DIR}/minerva2d/data"

/* This variable contains the path to the plugins install dir */
#define MINERVA2D_PLUGINS_DIR_FOR_TESTS "${CMAKE_INSTALL_PREFIX}/${MINERVA2D_PLUGIN_INSTALL_DIR}"
