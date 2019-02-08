.PHONY: auto build test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	local/bin/pip install -r requirements.txt

build34:
	virtualenv local --python=python3.4
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

test:
	rm -f .coverage
	. local/bin/activate && nosetests

docs:
	touch docs/index.rst
	cd docs; make html

clean:
	rm -rf local
	rm -f arrow/*.pyc tests/*.pyc
	rm -f .coverage

