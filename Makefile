.PHONY: auto test docs clean

auto: build27

build27: PYTHON_VER = python2.7
build35: PYTHON_VER = python3.5
build36: PYTHON_VER = python3.6
build37: PYTHON_VER = python3.7
build38: PYTHON_VER = python3.8

build27 build35 build36 build37 build38:
	virtualenv venv --python=$(PYTHON_VER)
	venv/bin/pip install -r requirements.txt
	venv/bin/pre-commit install

test:
	rm -f .coverage
	. venv/bin/activate && nosetests

lint:
	venv/bin/pre-commit run --all-files --show-diff-on-failure

docs:
	. venv/bin/activate && cd docs; make html

clean:
	rm -rf venv .tox ./**/__pycache__
	rm -rf dist build .egg .eggs arrow.egg-info
	rm -f ./**/*.pyc .coverage

publish:
	rm -rf dist build .egg .eggs arrow.egg-info
	pip3 install -U setuptools twine wheel
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -rf dist build .egg .eggs arrow.egg-info
