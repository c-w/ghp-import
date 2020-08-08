#!/usr/bin/env python

import io
import os

from markdown import markdown


def main():
    base = os.path.abspath(os.path.dirname(__file__))

    readme_path = os.path.join(os.path.dirname(base), "README.md")
    with io.open(readme_path, encoding="utf-8") as fobj:
        readme = fobj.read()

    template_path = os.path.join(base, "index.html.tmpl")
    with io.open(template_path, encoding="utf-8") as fobj:
        template = fobj.read()

    index_path = os.path.join(base, "index.html")
    with io.open(index_path, mode="w", encoding="utf-8") as fobj:
        html = markdown(readme, extensions=["fenced_code"])
        fobj.write(template.format(body=html))


if __name__ == "__main__":
    main()
