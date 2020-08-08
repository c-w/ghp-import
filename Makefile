DOCS_BRANCH := gh-pages
DOCS_REMOTE := origin

install:
	pip install -r requirements-dev.txt
	pip install -e .

lint:
	flake8 ./ghp_import.py ./setup.py ./docs/build.py

docs:
	./docs/build.py > docs/index.html
	./ghp_import.py -p docs/ -b $(DOCS_BRANCH) -r $(DOCS_REMOTE)

clean:
	python -c "import os; os.remove(os.path.join('docs', 'index.html'))"
	git branch -D $(DOCS_BRANCH)
	git push $(DOCS_REMOTE) --delete $(DOCS_BRANCH)

.PHONY: docs lint install clean
