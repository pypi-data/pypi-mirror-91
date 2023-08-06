#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

NAME = "confultimate"
VERSION = "0.1.1"
REQUIRES = ["pyyaml==5.3.1", "jsonmerge==1.7.0"]
TESTS_REQUIRES = ["pytest==5.4.3", "pytest-cov==2.10.0", "pytest-resource-path==1.2.1"]

setup(
    name=NAME,
    version=VERSION,
    description="confultimate",
    author="Escande Guillaume",
    author_email="escande.guillaume@gmail.com",
    url="https://github.com/GuillaumeEscande/confultimate",
    keywords=["conf"],
    install_requires=REQUIRES,
    tests_require=TESTS_REQUIRES,
    packages=find_packages(),
    package_data={},
    include_package_data=True,
    entry_points={
    }
)
