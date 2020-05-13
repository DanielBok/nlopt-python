FROM ubuntu:16.04

RUN apt-get update -y && \
    apt install -y software-properties-common python3-pip && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update

ARG PY_VER

RUN apt install -y python$PY_VER
