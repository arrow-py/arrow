.PHONY: auto build test docs clean

auto: build

build:
	virtualenv local
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

