set(kritadbexplorer_SOURCES
    DbExplorer.cpp
    DlgDbExplorer.cpp
    TableModel.cpp
)

ki18n_wrap_ui(kritadbexplorer_SOURCES WdgDbExplorer.ui )

kis_add_library(kritadbexplorer MODULE ${kritadbexplorer_SOURCES})

target_link_libraries(kritadbexplorer
    PRIVATE
        kritaresources
        kritaresourcewidgets
        kritaui
        Qt${QT_MAJOR_VERSION}::Core
        Qt${QT_MAJOR_VERSION}::Widgets
        Qt${QT_MAJOR_VERSION}::Sql
)
install(TARGETS kritadbexplorer DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})
install(FILES dbexplorer.xmlgui DESTINATION ${KDE_INSTALL_DATADIR}/minerva2dplugins)
install(FILES dbexplorer.action DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/actions)
