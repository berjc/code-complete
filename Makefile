.DELETE_ON_ERROR:

all:


test:
	py.test tests

coverage:


clean:
	rm -rf build/ dist/ .tox/
	cp examples/arithmetic/example.py.copy examples/arithmetic/example.py
	cp examples/sort_list/example.py.copy examples/sort_list/example.py
	cp examples/open_file/example.py.copy examples/open_file/example.py
	cp examples/data_science_workflow/example.py.copy examples/data_science_workflow/example.py
	find . -name '*.pyc' -delete
	find . -name '*.original' -delete
	find . -name '*.previous' -delete
	find . -name '__pycache__' -delete

.PHONY: all test clean
