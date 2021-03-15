DOCS_BRANCH := gh-pages
DOCS_REMOTE := origin
DOCS_OPTS := -p

install:
	pip install -e .[dev]

lint:
	flake8 ./ghp_import.py ./setup.py ./docs/build.py

docs:
	python ./docs/build.py
	ghp-import $(DOCS_OPTS) docs/ -b $(DOCS_BRANCH) -r $(DOCS_REMOTE) -m "Update docs [skip ci]" -o

clean:
	python -c "import os; os.remove(os.path.join('docs', 'index.html'))"
	git branch -D $(DOCS_BRANCH)
	git push $(DOCS_REMOTE) --delete $(DOCS_BRANCH)

release:
	python setup.py sdist
	twine upload --skip-existing --non-interactive ./dist/*

.PHONY: docs lint install clean release
