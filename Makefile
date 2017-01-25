.PHONY: auto build test docs clean

auto: build27

build27:
	virtualenv local --python=python2.7
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/python setup.py develop

build26:
	virtualenv local --python=python2.6
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/pip install --use-mirrors -r requirements26.txt
	local/bin/python setup.py develop

build33:
	virtualenv local --python=python3.3
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/python setup.py develop

build34:
	virtualenv local --python=python3.4
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/python setup.py develop


build35:
	virtualenv local --python=python3.5
	local/bin/pip install --use-mirrors -r requirements.txt
	local/bin/python setup.py develop

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

