#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = {}
with open("syncfin/__init__.py") as fp:
    exec(fp.read(), version)


setuptools.setup(
    name="syncfin",
    version=version['__version__'],
    author="Vipin Sharma",
    author_email="sh.vipin@gmail.com",
    description="Synchronized Finance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitvipin/syncfin",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
