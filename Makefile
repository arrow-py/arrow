.PHONY: auto build test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	python setup.py develop
	local/bin/pip install --use-mirrors -r requirements.txt

build26:
	virtualenv local --python=python2.6
	python setup.py develop
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/pip install --use-mirrors -r requirements26.txt

build33:
	virtualenv local --python=python3.3
	python setup.py develop
	local/bin/pip install --use-mirrors -r requirements.txt

build34:
	virtualenv local --python=python3.4
	python setup.py develop
	local/bin/pip install --use-mirrors -r requirements.txt


build35:
	virtualenv local --python=python3.5
	python setup.py develop
	local/bin/pip install --use-mirrors -r requirements.txt

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

