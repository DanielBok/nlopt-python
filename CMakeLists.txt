cmake_minimum_required(VERSION 3.1.0..3.12)

project(nlopt-python)

set (CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_BINARY_DIR})
set (CMAKE_INSTALL_LIBDIR ${CMAKE_INSTALL_PREFIX}/nlopt)
set (INSTALL_PYTHON_DIR ${CMAKE_INSTALL_PREFIX})

option (BUILD_SHARED_LIBS OFF)

find_package (PythonInterp)

execute_process(
  COMMAND
    ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())"
  OUTPUT_VARIABLE
    PYTHON_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
execute_process(
  COMMAND
    ${PYTHON_EXECUTABLE} -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))"
  OUTPUT_VARIABLE
    PYTHON_LIBRARY
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

set (PYTHON_INCLUDE_DIR ${PYTHON_INCLUDE_DIR} CACHE STRING "" FORCE)
set (PYTHON_LIBRARY ${PYTHON_LIBRARY} CACHE STRING "" FORCE)

message(STATUS "Found Python includes: ${PYTHON_INCLUDE_DIR}")
message(STATUS "Found Python libs: ${PYTHON_LIBRARY}")

add_subdirectory(extern/nlopt)
