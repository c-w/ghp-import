install:
	pip install -r requirements-dev.txt
	pip install -e .

lint:
	flake8 ./ghp_import.py ./setup.py ./docs/build.py

docs:
	./docs/build.py > docs/index.html
	./ghp_import.py -p docs/

.PHONY: docs lint install
