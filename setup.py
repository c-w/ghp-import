import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

LONG_DESC = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()

setup(
    name = "ghp-import",
    version = "0.1.2",
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
    ],
   
    scripts = ['ghp-import']
)
