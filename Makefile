.DELETE_ON_ERROR:

all:


test:


clean:
	rm -rf build/ dist/ .tox/
	find . -name '*.pyc' -delete
	find . -name '*.original' -delete
	find . -name '*.previous' -delete
	find . -name '__pycache__' -delete

.PHONY: all test clean
