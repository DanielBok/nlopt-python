#!/bin/bash

set -e -x

# things to note: the /tmp folder is a shared volume with the git repository of
# the checked out codes on travis. Thus you will see things /tmp/setup.py,
# /tmp/nlopt/*, etc.

PY_VER="${PY_VER:-37}"
PATH=/opt/python/cp${PY_VER}-cp${PY_VER}m/bin:$PATH

# Go to root and setup nlopt
cd /
NL_SRC=/stevengj/nlopt
git clone https://github.com/stevengj/nlopt ${NL_SRC}
PREFIX=${NL_SRC}/install

cd ${NL_SRC}
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
make
make install

# copies the generated binaries and python codes to the tmp folder
# cp which ignores the "cp -i" interactive option set in the .bashrc
\cp -f ${PREFIX}/lib/python3.7/site-packages/* /app/nlopt/

PLAT=manylinux2010_x86_64

cd /app
# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" wheel /app -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" --plat ${PLAT} -w /app/wheelhouse/
done
