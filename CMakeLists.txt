cmake_minimum_required(VERSION 3.1.0..3.12)

project(nlopt-python)

set (CMAKE_INSTALL_PREFIX ${CMAKE_CURRENT_BINARY_DIR})
set (CMAKE_INSTALL_LIBDIR ${CMAKE_INSTALL_PREFIX}/nlopt)
set (INSTALL_PYTHON_DIR ${CMAKE_INSTALL_PREFIX})

option (BUILD_SHARED_LIBS OFF)

add_subdirectory(extern/nlopt)

set (NLOPT_PYTHON ON)
