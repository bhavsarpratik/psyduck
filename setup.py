#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'psyduck'
DESCRIPTION = 'Utility library for ML projects'
URL = 'https://github.com/bhavsarpratik/psyduck'
EMAIL = 'pratik.a.bhavsar@gmail.com'
AUTHOR = 'Pratik Bhavsar'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md')) as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, 'psy', '__version__.py')) as f:
    exec(f.read(), about)

# Load requirements file
required = {}
with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

setup(
    name=NAME,
    version=about['__version__'],
    license='MIT',
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    download_url='',
    keywords=['SOME', 'MEANINGFULL', 'KEYWORDS'],
    packages=find_packages(exclude=('tests', 'bin')),
    test_suite='tests',
    install_requires=required,
    include_package_data=True,  # all files and directories listed in MANIFEST.in.
    zip_safe=False,  # the package can run out of an .egg file
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ]
)
