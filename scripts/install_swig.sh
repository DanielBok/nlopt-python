#!/bin/sh
yum update -y && yum install pcre-devel -y

cd /tmp
if [ ! -e swig.tar.gz ]; then # helps during debugging...
  curl -L https://sourceforge.net/projects/swig/files/swig/swig-4.0.2/swig-4.0.2.tar.gz/download --output swig.tar.gz
fi

rm -rf /tmp/swig
mkdir swig

tar -xvzf /tmp/swig.tar.gz -C swig --strip-components 1
cd swig
./configure --without-alllang --with-python3 && make -j2 && make install
