import os
import sys
from io import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), "README.md"), 'r', encoding='utf-8').read()

setup(
    name = "ghp-import",
    version = "0.4.1",
    description = "Copy your docs directly to the gh-pages branch.",
    long_description = LONG_DESC,
    author = "Paul Joseph Davis",
    author_email = "paul.joseph.davis@gmail.com",
    license = "Tumbolia Public License",
    url = "http://github.com/davisp/ghp-import",
    zip_safe = False,

    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    scripts = ['ghp-import']
)
