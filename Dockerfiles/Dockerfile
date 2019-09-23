FROM quay.io/pypa/manylinux1_x86_64

ARG CMAKE_VERSION=2.8.12.2

RUN yum update -y && yum install pcre-devel gcc dos2unix -y
RUN curl -o /var/cmake.tar.gz https://cmake.org/files/v2.8/cmake-${CMAKE}.tar.gz && \
    cd cmake-${CMAKE_VERSION} && \
    ./bootstrap --prefix=/usr/local && \
    make && \
    make install

ENV PATH="/usr/local/bin:${PATH}"

WORKDIR /tmp
RUN curl -L https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz/download --output swig.tar.gz
RUN mkdir -p swig && tar -xvzf swig.tar.gz -C swig --strip-components 1

WORKDIR /tmp/swig
RUN ./configure && make && make install

WORKDIR /tmp
RUN rm -rf ./*

ENV PATH="/usr/local/bin/swig:$PATH"

WORKDIR /
ENTRYPOINT ["bash"]
