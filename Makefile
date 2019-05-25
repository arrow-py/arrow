.PHONY: auto test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	local/bin/pip install -r requirements.txt

build35:
	virtualenv local --python=python3.5
	local/bin/pip install -r requirements.txt

build36:
	virtualenv local --python=python3.6
	local/bin/pip install -r requirements.txt

build37:
	virtualenv local --python=python3.7
	local/bin/pip install -r requirements.txt

build38:
	virtualenv local --python=python3.8
	local/bin/pip install -r requirements.txt

test:
	rm -f .coverage
	. local/bin/activate && nosetests

lint:
	local/bin/pip install -U pre-commit
	pre-commit install && pre-commit run --all-files --show-diff-on-failure

# flake8:
# 	local/bin/flake8 arrow tests setup.py

# check-formatting: flake8
# 	local/bin/black arrow tests setup.py --check --diff --target-version py27
# 	local/bin/isort -rc arrow tests setup.py --check-only --diff --virtual-env local

# fix-formatting:
# 	local/bin/black arrow tests setup.py --target-version py27
# 	local/bin/isort -rc arrow tests setup.py --virtual-env local

docs:
	touch docs/index.rst
	cd docs; make html

clean:
	rm -rf local ./**/__pycache__
	rm -f ./**/*.pyc .coverage
