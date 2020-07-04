cmake_minimum_required(VERSION 3.1.0)
project(nlopt-python)

add_subdirectory(extern/nlopt)

set (NLOPT_PYTHON ON)
set (NLOPT_OCTAVE OFF)
set (NLOPT_MATLAB OFF)
set (NLOPT_GUILE OFF)
