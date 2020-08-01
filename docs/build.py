#!/usr/bin/env python

import io
import os

from markdown import markdown


def main():
    base = os.path.abspath(os.path.dirname(__file__))

    readme_path = os.path.join(os.path.dirname(base), "README.md")
    readme = io.open(readme_path, encoding="utf-8").read()

    template_path = os.path.join(base, "index.html.tmpl")
    template = io.open(template_path, encoding="utf-8").read()

    print(template.format(body=markdown(readme)))


if __name__ == "__main__":
    main()
