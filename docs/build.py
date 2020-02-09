#!/usr/bin/env python

import os
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO    

import markdown


def main():
    base = os.path.abspath(os.path.dirname(__file__))
    index = os.path.join(base, "index.html.tmpl")
    readme = os.path.join(os.path.dirname(base), "README.md")

    templ = open(index).read()

    buf = StringIO("rw")
    markdown.markdownFromFile(input=readme, output=buf)

    print(templ.format(body=buf.getvalue()))

if __name__ == '__main__':
    main()
