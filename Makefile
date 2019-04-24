.PHONY: all clean build repub

VERSION := 2.6.1

all: clean build
	@echo Done!

build:
	# for testing purposes
	python setup.py bdist_wheel -p win_amd64 --python-tag py37

clean:
	rm -rf build dist *.egg-info
	rm -f nlopt/_nlopt.* nlopt/*.dll
	rm -rf wheelhouse

repub:
	git tag --delete $(VERSION)
	git tag -a $(VERSION) -m "NLOpt $(VERSION)"
	git push -f
	git push -f --tags
