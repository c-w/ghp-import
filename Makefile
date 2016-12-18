
docs:
	pyflakes ./ghp_import.py
	./docs/build.py > docs/index.html
	./ghp_import.py -p docs/


.PHONY: docs
