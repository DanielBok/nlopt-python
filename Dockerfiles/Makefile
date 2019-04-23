.PHONY: build push

all: build push

build:
	docker image build -t danielbok/manylinux2010_x86_64:latest -f manylinux2010_x86_64.Dockerfile .

push:
	docker push danielbok/manylinux2010_x86_64:latest
