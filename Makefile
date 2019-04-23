.PHONY: all clean build

all: clean build
	@echo Done!

build:
	# for testing purposes
	python setup.py bdist_wheel -p win_amd64 --python-tag py37

clean:
	rm -rf build dist *.egg-info
