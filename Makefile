.PHONY: auto test docs clean

auto: build27

build27: PYTHON_VER = python2.7
build35: PYTHON_VER = python3.5
build36: PYTHON_VER = python3.6
build37: PYTHON_VER = python3.7
build38: PYTHON_VER = python3.8

build27 build35 build36 build37 build38:
	virtualenv local --python=$(PYTHON_VER)
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

test:
	rm -f .coverage
	. local/bin/activate && nosetests

test-dev:
	rm -f .coverage
	. local/bin/activate && python -Wd -m nose

lint:
	local/bin/pre-commit run --all-files --show-diff-on-failure

docs:
	touch docs/index.rst
	. local/bin/activate && cd docs; make html

clean:
	rm -rf local .tox ./**/__pycache__
	rm -rf dist build .egg arrow.egg-info
	rm -f ./**/*.pyc .coverage
