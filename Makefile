.PHONY: auto build test clean

auto: build

build:
	virtualenv local
	local/bin/pip install -r requirements.txt

test:
	. local/bin/activate && nosetests --all-modules --with-coverage arrow tests

clean:
	rm -rf local
	rm -f arrow/*.pyc tests/*.pyc

