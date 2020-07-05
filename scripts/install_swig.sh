#!/bin/sh
if [ ! -e /tmp/swig.tar.gz ]; then
  # only do this once

  curl -L https://sourceforge.net/projects/swig/files/swig/swig-4.0.2/swig-4.0.2.tar.gz/download --output /tmp/swig.tar.gz
fi

if [ ! -e /tmp/swig ]; then
  # only do this once

  yum update -y && yum install pcre-devel -y

  mkdir /tmp/swig
  tar -xvzf /tmp/swig.tar.gz -C /tmp/swig --strip-components 1 &> /dev/null

  pushd /tmp/swig
  ./configure --without-alllang --with-python3 && make -j2 && make install > /dev/null
  popd
fi
