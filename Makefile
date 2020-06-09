.PHONY: auto test docs clean

auto: build38

build36: PYTHON_VER = python3.6
build37: PYTHON_VER = python3.7
build38: PYTHON_VER = python3.8

build36 build37 build38: clean
	virtualenv venv --python=$(PYTHON_VER)
	. venv/bin/activate; \
	pip install -r requirements.txt; \
	pre-commit install

test:
	rm -f .coverage
	. venv/bin/activate; pytest

lint:
	. venv/bin/activate; pre-commit run --all-files --show-diff-on-failure

docs:
	rm -rf docs/_build
	. venv/bin/activate; cd docs; make html

clean: clean-dist
	rm -rf venv .pytest_cache ./**/__pycache__
	rm -f .coverage ./**/*.pyc

clean-dist:
	rm -rf dist build .egg .eggs arrow.egg-info

build-dist:
	. venv/bin/activate; \
	pip install -U setuptools twine wheel; \
	python setup.py sdist bdist_wheel

upload-dist:
	. venv/bin/activate; twine upload dist/*

publish: test clean-dist build-dist upload-dist clean-dist
