
docs:
	./docs/build.py > docs/index.html
	./ghp-import -p docs/


.PHONY: docs
