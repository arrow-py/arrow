.PHONY: auto test docs clean

auto: build311

build38: PYTHON_VER = python3.8
build39: PYTHON_VER = python3.9
build310: PYTHON_VER = python3.10
build311: PYTHON_VER = python3.11
build312: PYTHON_VER = python3.12
build313: PYTHON_VER = python3.13

build36 build37 build38 build39 build310 build311 build312 build313: clean
	$(PYTHON_VER) -m venv venv
	. venv/bin/activate; \
	pip install -U pip setuptools wheel; \
	pip install -r requirements/requirements-tests.txt; \
	pip install -r requirements/requirements-docs.txt; \
	pre-commit install

test:
	rm -f .coverage coverage.xml
	. venv/bin/activate; \
	pytest

lint:
	. venv/bin/activate; \
	pre-commit run --all-files --show-diff-on-failure

clean-docs:
	rm -rf docs/_build

docs:
	. venv/bin/activate; \
	cd docs; \
	make html

live-docs: clean-docs
	. venv/bin/activate; \
	sphinx-autobuild docs docs/_build/html

clean: clean-dist
	rm -rf venv .pytest_cache ./**/__pycache__
	rm -f .coverage coverage.xml ./**/*.pyc

clean-dist:
	rm -rf dist build *.egg *.eggs *.egg-info

build-dist: clean-dist
	. venv/bin/activate; \
	pip install -U flit; \
	flit build
