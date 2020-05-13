#!/bin/bash

# things to note: the /tmp folder is a shared volume with the git repository of
# the checked out codes on travis. Thus you will see things /tmp/setup.py,
# /tmp/nlopt/*, etc.

PY_VER="${PY_VER:-37}"
PLAT="${PLAT:-manylinux1_x86_64}"

if [ $PY_VER = "37" ]; then
  PATH=/opt/python/cp${PY_VER}-cp${PY_VER}m/bin:$PATH
elif [ $PY_VER = "38" ]; then
  PATH=/opt/python/cp${PY_VER}-cp${PY_VER}/bin:$PATH
else
  echo "Unsupported python version: ${PY_VER}"
  exit 1
fi

NL_SRC=/stevengj/nlopt
PREFIX=${NL_SRC}/install

echo "
Python Version = ${PY_VER}
Platform       = ${PLAT}
"

# Go to root and setup nlopt
cd /

git clone https://github.com/stevengj/nlopt ${NL_SRC}
cd ${NL_SRC}
mkdir build && cd build
pip install numpy # numpy is needed to generate python code

# generate the python codes
cmake -DCMAKE_PREFIX_PATH=${PREFIX} \
  -DCMAKE_INSTALL_PREFIX=${PREFIX} \
  -DCMAKE_INSTALL_LIBDIR=lib \
  -DNLOPT_GUILE=OFF \
  -DNLOPT_MATLAB=OFF \
  -DNLOPT_OCTAVE=OFF \
  -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_LIBRARY=$(python -c "import distutils.sysconfig as sysconfig; print(sysconfig.get_config_var('LIBDIR'))") \
  ..

# generate the .so binaries
make && make install

# copies the generated binaries and python codes to the tmp folder
# cp which ignores the "cp -i" interactive option set in the .bashrc
\cp -f ${PREFIX}/lib/python${PY_VER:0:1}.${PY_VER:1:2}/site-packages/* /app/nlopt/

# Compile wheels
cd /app
python setup.py bdist_wheel --python-tag cp${PY_VER} --plat-name linux_x86_64 --dist-dir /wheelhouse

# Bundle external shared libraries into the wheels
for whl in /wheelhouse/nlopt-*.whl; do
  auditwheel repair "$whl" --plat ${PLAT} -w /app/dist/
done
