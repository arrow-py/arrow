.PHONY: auto build test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	local/bin/pip install -r requirements.txt

build26:
	virtualenv local --python=python2.6
	local/bin/pip install -r requirements.txt

test:
	rm -f .coverage
	. local/bin/activate && nosetests --all-modules --with-coverage arrow tests

docs:
	touch docs/index.rst
	cd docs; make html

clean:
	rm -rf local
	rm -f arrow/*.pyc tests/*.pyc
	rm -f .coverage

