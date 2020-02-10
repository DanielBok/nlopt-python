FROM quay.io/pypa/manylinux1_x86_64

ARG CMAKE_VERSION=2.8.12.2

RUN yum update -y && yum install pcre-devel gcc dos2unix -y

WORKDIR /
# Install cmake
RUN curl -o /var/cmake.tar.gz -L https://cmake.org/files/v2.8/cmake-${CMAKE_VERSION}.tar.gz && \
    mkdir -p cmake-${CMAKE_VERSION} && \
    tar -xvzf /var/cmake.tar.gz -C cmake-${CMAKE_VERSION} --strip-components 1 && \
    cd cmake-${CMAKE_VERSION} && \
    ./bootstrap --prefix=/usr/local && \
    make && \
    make install

WORKDIR /
# Install swig
RUN curl -L https://sourceforge.net/projects/swig/files/swig/swig-3.0.12/swig-3.0.12.tar.gz/download --output /var/swig.tar.gz && \
    mkdir -p swig && \
    tar -xvzf /var/swig.tar.gz -C swig --strip-components 1 && \
    cd swig && \
    ./configure && \
    make && \
    make install

WORKDIR /
RUN rm -rf cmake-${CMAKE_VERSION} swig

RUN /opt/python/cp36-cp36m/bin/pip install -U pip numpy cython scipy
RUN /opt/python/cp37-cp37m/bin/pip install -U pip numpy cython scipy
RUN /opt/python/cp38-cp38/bin/pip install -U pip numpy cython scipy

ENTRYPOINT ["bash"]
