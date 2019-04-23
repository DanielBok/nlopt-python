FROM quay.io/pypa/manylinux2010_x86_64

RUN yum update -y &&  yum install pcre-devel cmake3 -y

WORKDIR /tmp
RUN curl -L https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz/download --output swig.tar.gz
RUN mkdir -p swig && tar -xvzf swig.tar.gz -C swig --strip-components 1

WORKDIR /tmp/swig
RUN ./configure && make && make install

WORKDIR /tmp
RUN rm -rf ./*

ENV PATH="/usr/local/bin/swig:$PATH"

WORKDIR /
