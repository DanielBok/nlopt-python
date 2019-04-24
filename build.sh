#!/bin/bash

set -e -x

# things to note: the /tmp folder is a shared volume with the git repository of
# the checked out codes on travis. Thus you will see things /tmp/setup.py,
# /tmp/nlopt/*, etc.

PY_VER="${PY_VER:-37}"
PLAT=${PLAT:-manylinux2010_x86_64}
PATH=/opt/python/cp${PY_VER}-cp${PY_VER}m/bin:$PATH
NLOPT_TAG=v2.6.1

# Go to root and setup nlopt
cd /
NL_SRC=/stevengj/nlopt
PREFIX=${NL_SRC}/install

git clone https://github.com/stevengj/nlopt ${NL_SRC}
cd ${NL_SRC}
git checkout ${NLOPT_TAG}
mkdir build && cd build
pip install numpy  # numpy is needed to generate python code

# generate the python codes
cmake -DCMAKE_PREFIX_PATH=${PREFIX} \
    -DCMAKE_INSTALL_PREFIX=${PREFIX} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DNLOPT_GUILE=OFF \
    -DNLOPT_MATLAB=OFF \
    -DNLOPT_OCTAVE=OFF \
    -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())")  \
    -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
    ..

# generate the .so binaries
make && make install

# copies the generated binaries and python codes to the tmp folder
# cp which ignores the "cp -i" interactive option set in the .bashrc
\cp -f ${PREFIX}/lib/python3.7/site-packages/* /app/nlopt/

# Compile wheels
for PY_VER in "36" "37"; do
    "/opt/python/cp${PY_VER}-cp${PY_VER}m/bin/pip" wheel /app -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat ${PLAT} -w /app/wheelhouse/
done

# remove all numpy wheels, keep only many linux wheel
rm -f /app/wheelhouse/numpy*.whl nlopt-*-py*-any.whl
