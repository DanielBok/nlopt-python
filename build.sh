#!/bin/bash

set -e -x

APP_DIR="${APP_DIR:-/}"
PY_VER="${PY_VER:-37}"
PATH=/opt/python/cp${PY_VER}-cp${PY_VER}m/bin:$PATH

cd /
NL_SRC=_nlopt_
git clone https://github.com/stevengj/nlopt ${NL_SRC}
PREFIX=/${NL_SRC}/install

cd ${NL_SRC}/
mkdir build && cd build
pip install numpy

cmake -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DNLOPT_GUILE=OFF \
    -DNLOPT_MATLAB=OFF \
    -DNLOPT_OCTAVE=OFF \
    -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
    -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
    ..

make install

# cp which ignores the "cp -i" interactive option set in the .bashrc
\cp -f /${NL_SRC}/install/lib/python3.7/site-packages/* ${APP_DIR}/nlopt/

PLAT=manylinux2010_x86_64

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" wheel /nlopt-python -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat ${PLAT} -w /nlopt-python/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install nlopt --no-index -f /nlopt-python/wheelhouse
done
