#!/bin/sh
cd /tmp
curl -L https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz/download --output swig.tar.gz
rm -rf /tmp/swig
mkdir swig
tar -xvzf /tmp/swig.tar.gz -C swig --strip-components 1
cd swig
./configure && make && make install
