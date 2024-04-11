cmake_minimum_required(VERSION 3.0.0)
project(azure-nvme-utils VERSION 0.1.0 LANGUAGES C)

include(cmake/cppcheck.cmake)
include(cmake/clangformat.cmake)

include(CTest)
enable_testing()

add_compile_options(-Wextra -Wall -Werror -std=gnu11 -D_GNU_SOURCE=1)
add_executable(azure-nvme-id src/main.c)

option(AZURE_LUN_CALCULATION_BY_NSID_ENABLED "Enable fallback \"LUN\" calculation via NSID" ON)
if(AZURE_LUN_CALCULATION_BY_NSID_ENABLED)
    set(AZURE_LUN_CALCULATION_BY_NSID_ENABLED 1)
else()
    set(AZURE_LUN_CALCULATION_BY_NSID_ENABLED 0)
endif()

configure_file(
  "${PROJECT_SOURCE_DIR}/udev/80-azure-nvme.rules.in"
  "${PROJECT_SOURCE_DIR}/udev/80-azure-nvme.rules"
  @ONLY
)

if(NOT DEFINED VERSION)
    execute_process(
        COMMAND git describe --tags --always --dirty
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        OUTPUT_VARIABLE VERSION
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
endif()

configure_file(
    "${CMAKE_SOURCE_DIR}/src/version.h.in"
    "${CMAKE_SOURCE_DIR}/src/version.h"
    @ONLY
)

configure_file(
    "${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1.md.in"
    "${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1.md"
    @ONLY
)

find_program(PANDOC_EXECUTABLE pandoc)

if(PANDOC_EXECUTABLE)
    add_custom_command(
        OUTPUT ${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1
        COMMAND ${PANDOC_EXECUTABLE}
            ${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1.md
            -s -t man
            -o ${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1
        DEPENDS ${CMAKE_SOURCE_DIR}/doc/azure-nvme-id.1.md
        COMMENT "Generating manpage for azure-nvme-id"
    )

    add_custom_target(
        GenerateMan ALL
        DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/doc/azure-nvme-id.1
    )
else()
    message(WARNING "Pandoc not found, will not generate manpages")
endif()

set(AZURE_NVME_ID_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/sbin")
set(MANPAGES_INSTALL_DIR "${CMAKE_INSTALL_PREFIX}/share/man")
set(UDEV_RULES_INSTALL_DIR "/lib/udev/rules.d")

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/doc/azure-nvme-id.1
        DESTINATION ${MANPAGES_INSTALL_DIR}/man1)
install(TARGETS azure-nvme-id DESTINATION ${AZURE_NVME_ID_INSTALL_DIR})
install(FILES udev/80-azure-nvme.rules DESTINATION ${UDEV_RULES_INSTALL_DIR})

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
