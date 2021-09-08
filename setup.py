# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages


README = 'Production (no README available)'
if os.path.isfile('README.md'):
    with open('README.md') as f:
        README = f.read()

setup(
    name='avito-matrix',
    version='0.1.0',
    description='Read square matrix from remote server and transform it into a vector',
    long_description=README,
    packages=find_packages(exclude=('tests')),
    py_modules=['avito_matrix'],
    test_requires=[
        'pytest',
    ],
)
