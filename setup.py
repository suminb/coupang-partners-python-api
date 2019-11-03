#!/usr/bin/env python

import setuptools
from distutils.core import setup
import coupang.partners


def readme():
    try:
        with open("README.rst") as f:
            return f.read()
    except:
        return "(Could not read from README.rst)"


setup(
    name="coupang-partners-python-api",
    py_modules=["coupang"],
    version=coupang.partners.__version__,
    description="Coupang Partners Python API",
    long_description=readme(),
    author="Sumin Byeon",
    author_email="suminb@gmail.com",
    url="https://github.com/suminb/coupang-partners-python-api",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
