add_subdirectory(tests)

set(kritapdfimport_SOURCES kis_pdf_import.cpp kis_pdf_import_widget.cpp )

ki18n_wrap_ui(kritapdfimport_SOURCES pdfimportwidgetbase.ui )

kis_add_library(kritapdfimport MODULE ${kritapdfimport_SOURCES})

target_link_libraries(kritapdfimport kritaui Poppler::Qt${QT_MAJOR_VERSION})

install(TARGETS kritapdfimport  DESTINATION ${MINERVA2D_PLUGIN_INSTALL_DIR})

install(FILES minerva2d_pdf.desktop DESTINATION ${KDE_INSTALL_APPDIR})
