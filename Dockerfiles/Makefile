.PHONY: build push

IMAGE_NAME = danielbok/manylinux1_x86_64

all: build push

build:
	docker image build -t $(IMAGE_NAME):latest .

push:
	docker push $(IMAGE_NAME):latest
