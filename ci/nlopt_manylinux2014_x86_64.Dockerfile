FROM quay.io/pypa/manylinux2014_x86_64:2020-12-25-6634688

# cmake already version 3, thus no need to update cmake

# add swig
RUN yum update -y && \
    curl -L https://sourceforge.net/projects/swig/files/swig/swig-4.0.2/swig-4.0.2.tar.gz/download --output /tmp/swig.tar.gz && \
    mkdir -p /tmp/swig && \
    tar -xvzf /tmp/swig.tar.gz -C /tmp/swig --strip-components 1 &> /dev/null && \
    pushd /tmp/swig && \
    ./configure --without-alllang --with-python3 && make -j2 && make install > /dev/null && \
    popd
