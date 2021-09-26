import io
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

HERE = os.path.dirname(__file__)
LONG_DESC_PATH = os.path.join(HERE, "README.md")
LONG_DESC = io.open(LONG_DESC_PATH, encoding="utf-8").read()

with io.open(os.path.join(HERE, "ghp_import.py"), encoding="utf-8") as fobj:
    for line in fobj:
        match = re.match(
            r"^__version__\s*=\s*['\"](?P<version>[\d.]+)['\"]$",
            line.strip()
        )
        if match:
            VERSION = match.group("version")
            break

setup(
    name="ghp-import",
    version=VERSION,
    description="Copy your docs directly to the gh-pages branch.",
    long_description=LONG_DESC,
    long_description_content_type="text/markdown",
    author="Paul Joseph Davis",
    author_email="paul.joseph.davis@gmail.com",
    license="Apache Software License",
    url="https://github.com/c-w/ghp-import",
    zip_safe=False,

    install_requires=[
        "python-dateutil>=2.8.1",
    ],

    extras_require={
        "dev": [
            "twine",
            "markdown",
            "flake8",
            "wheel",
        ],
    },

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],

    py_modules=["ghp_import"],

    entry_points={
        "console_scripts": [
            "ghp-import = ghp_import:main",
        ],
    }
)
