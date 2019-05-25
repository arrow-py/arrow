.PHONY: auto test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build35:
	virtualenv local --python=python3.5
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build36:
	virtualenv local --python=python3.6
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build37:
	virtualenv local --python=python3.7
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

build38:
	virtualenv local --python=python3.8
	local/bin/pip install -r requirements.txt
	local/bin/pre-commit install

test:
	rm -f .coverage
	. local/bin/activate && nosetests

lint:
	local/bin/pre-commit run --all-files

lint-ci:
	local/bin/pre-commit run --all-files --show-diff-on-failure

docs:
	touch docs/index.rst
	cd docs; make html

clean:
	rm -rf local ./**/__pycache__
	rm -f ./**/*.pyc .coverage
