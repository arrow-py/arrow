.PHONY: docs

auto: docs

docs:
	cp -R ../arrow/docs/_build/html/* .
