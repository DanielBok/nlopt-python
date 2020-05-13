#!/bin/bash

versions=(3.7 3.8)
user=danielbok

for ver in "${versions[@]}"; do
  docker image build -t ${user}/ubuntu:${ver} -f ubuntu.Dockerfile --build-arg PY_VER=${ver} .
done
