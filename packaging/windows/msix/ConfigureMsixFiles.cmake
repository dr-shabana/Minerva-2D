# The MSIX packaging is only designed for x64

if(DEFINED MINERVA2D_STABLE)
    set(MSIX_DISPLAY_NAME_SUFFIX "")
else()
    set(MSIX_DISPLAY_NAME_SUFFIX " ${MINERVA2D_VERSION_STRING}")
    if(MINERVA2D_GIT_SHA1_STRING)
        set(MSIX_DISPLAY_NAME_SUFFIX "${MSIX_DISPLAY_NAME_SUFFIX} (git ${MINERVA2D_GIT_SHA1_STRING})")
    endif(MINERVA2D_GIT_SHA1_STRING)
endif()

configure_file(
    ${CMAKE_CURRENT_LIST_DIR}/manifest.xml.in
    ${CMAKE_CURRENT_BINARY_DIR}/manifest.xml
    @ONLY
)

install(
    FILES
        ${CMAKE_CURRENT_BINARY_DIR}/manifest.xml
        ${CMAKE_CURRENT_LIST_DIR}/build_msix.py
        ${CMAKE_CURRENT_LIST_DIR}/priconfig.xml
    DESTINATION
        ${CMAKE_INSTALL_PREFIX}/minerva2d-msix
)

install(
    DIRECTORY 
        ${CMAKE_CURRENT_LIST_DIR}/pkg
    DESTINATION
        ${CMAKE_INSTALL_PREFIX}/minerva2d-msix
)
