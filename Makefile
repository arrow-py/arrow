.PHONY: docs

auto: docs

docs:
	cp -R ../arrow/docs/_build/html/* .
	git commit -a -m "docs update"
	git push origin gh-pages
