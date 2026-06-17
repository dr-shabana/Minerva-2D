# SPDX-FileCopyrightText: 2012, 2013 Shaheed Haque <srhaque@theiet.org>
# SPDX-FileCopyrightText: 2013 Alex Turbov <i.zaufi@gmail.com>
# SPDX-FileCopyrightText: 2014-2016 Boudewijn Rempt <boud@valdyas.org>
#
# SPDX-License-Identifier: BSD-2-Clause

include(CMakeParseArguments)

#
# Simple helper function to install plugin and related files
# having only a name of the plugin...
# (just to reduce syntactic noise when a lot of plugins get installed)
#
function(install_pyminerva2d_plugin name)
    set(_options)
    set(_one_value_args)
    set(_multi_value_args PATTERNS FILE)
    cmake_parse_arguments(install_pyminerva2d_plugin "${_options}" "${_one_value_args}" "${_multi_value_args}" ${ARGN})
    if(NOT name)
        message(FATAL_ERROR "Plugin filename is not given")
    endif()
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${name}.py)
        install(FILES kritapyminerva2d_${name}.desktop DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d)
        foreach(_f ${name}.py ${name}.ui ${install_pyminerva2d_plugin_FILE})
            if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${_f})
                install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/${_f} DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d)
            endif()
        endforeach()
    elseif(IS_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${name})
        install(FILES ${name}/minerva2dpyminerva2d_${name}.desktop DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d)
        install(
            DIRECTORY ${name}
            DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d
            FILES_MATCHING
                PATTERN "*.py"
                PATTERN "*.ui"
                PATTERN "*.txt"
                PATTERN "*.csv"
                PATTERN "*.html"
                PATTERN "__pycache__*" EXCLUDE
                PATTERN "tests*" EXCLUDE
           )
        # TODO Is there any way to form a long PATTERN options string
        # and use it in a single install() call?
        # NOTE Install specified patterns one-by-one...
        foreach(_pattern ${install_pyminerva2d_plugin_PATTERNS})
            install(
                DIRECTORY ${name}
                DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d
                FILES_MATCHING
                    PATTERN "${_pattern}"
                    PATTERN "__pycache__*" EXCLUDE
		    PATTERN "tests*" EXCLUDE
              )
        endforeach()
    else()
        message(FATAL_ERROR "Do not know what to do with ${name}")
    endif()
endfunction()

install_pyminerva2d_plugin(assignprofiledialog)
install_pyminerva2d_plugin(scripter)
install_pyminerva2d_plugin(colorspace)
install_pyminerva2d_plugin(documenttools)
install_pyminerva2d_plugin(filtermanager)
install_pyminerva2d_plugin(exportlayers)
install_pyminerva2d_plugin(batch_exporter)
#install_pyminerva2d_plugin(highpass)
install_pyminerva2d_plugin(tenbrushes)
install_pyminerva2d_plugin(tenscripts)
install_pyminerva2d_plugin(palette_docker)
install_pyminerva2d_plugin(quick_settings_docker)
install_pyminerva2d_plugin(lastdocumentsdocker)
# install_pyminerva2d_plugin(scriptdocker)
install_pyminerva2d_plugin(comics_project_management_tools)
install_pyminerva2d_plugin(minerva2d_script_starter)
install_pyminerva2d_plugin(plugin_importer)
install_pyminerva2d_plugin(mixer_slider_docker)
install_pyminerva2d_plugin(mutator)
install_pyminerva2d_plugin(channels2layers)
install_pyminerva2d_plugin(photobash_images)
install_pyminerva2d_plugin(workflow_buttons)

# if(PYTHON_VERSION_MAJOR VERSION_EQUAL 3)
#     install_pyminerva2d_plugin(cmake_utils)
#     install_pyminerva2d_plugin(js_utils PATTERNS "*.json")
#     install_pyminerva2d_plugin(expand PATTERNS "*.expand" "templates/*.tpl")
# endif()

install( FILES
    tenbrushes/tenbrushes.action
    tenscripts/tenscripts.action
    plugin_importer/plugin_importer.action
    mutator/mutator.action
DESTINATION  ${KDE_INSTALL_DATADIR}/minerva2d/actions)

install(
    DIRECTORY libkritapyminerva2d
    DESTINATION ${KDE_INSTALL_DATADIR}/minerva2d/pyminerva2d
    FILES_MATCHING
        PATTERN "*.py"
        PATTERN "__pycache__*" EXCLUDE
  )
