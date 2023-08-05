# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whitebeam',
 'whitebeam.base',
 'whitebeam.core',
 'whitebeam.ensemble',
 'whitebeam.utils']

package_data = \
{'': ['*']}

install_requires = \
['Cython>=0.29.21,<0.30.0', 'joblib>=1.0.0,<2.0.0', 'numpy>=1.19.5,<2.0.0']

setup_kwargs = {
    'name': 'whitebeam',
    'version': '1.0.3',
    'description': 'Whitebeam is a framework for creating decision tree functions.',
    'long_description': '# whitebeam\n\n| | |\n|---------|---|\n| docs    | [![Documentation Status](https://readthedocs.org/projects/whitebeam/badge/?version=latest)](https://whitebeam.readthedocs.io/en/latest/?badge=latest) |\n| test    | [![Build Status](https://travis-ci.com/K-Molloy/whitebeam.svg?branch=main)](https://travis-ci.com/K-Molloy/whitebeam) [![Requirements Status](https://requires.io/github/K-Molloy/whitebeam/requirements.svg?branch=main)](https://requires.io/github/K-Molloy/whitebeam/requirements/?branch=main)  |\n| package | [![PythonVersion](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)  [![PyPI version](https://badge.fury.io/py/Whitebeam.svg)](https://badge.fury.io/py/Whitebeam) ![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/K-Molloy/whitebeam/latest) ![GitHub last commit](https://img.shields.io/github/last-commit/K-Molloy/whitebeam) [![codecov](https://codecov.io/gh/K-Molloy/whitebeam/branch/main/graph/badge.svg?token=KQDZUPH74N)](https://codecov.io/gh/K-Molloy/whitebeam)|\n\n**whitebeam** is a python module for decision trees without the use of sklearn and SciPy\n\nThe project was started in 2020 by Kieran Molloy as a coursework component for SCC461 at Lancaster University\n\n# Installation\n\n## Dependencies\n\nwhitebeam requires:\n\n- Python (>= 3.6)\n- NumPy (>= 1.14)\n- Cython (>= 0.29.21)\n- joblib (>= 1.0.0)\n\n## User Installation\n\nIf you already have a working directory, the easiest installation is via `pip`\n\n```\npip install whitebeam\n```\n\nHowever it is advisable to install within a virtual environment\n\n```\nvirtualenv venv\nvenv/bin/activate\npip install whitebeam\n```\n\nThere will soon be more detailed installation instructions in the docs.\n\n# Changelog\n\nSee the changelog for a history of notable changes to whitebeam\n\n# Development\n\nDevelopment is planned to be ongoing however this may change due to university requirements.\n\n## Source Installation\n\nInstalling from source requires `python-dev` which can be installed using \n```\nsudo apt-get install python3-dev\n```\nthen cloning this repo, installing requirements and building\n```\ngit clone https://github.com/K-Molloy/whitebeam\npip install -r requirements.txt\npython setup.py build_ext --inplace\n```\nagain, it is advisable to use a virtual environment.\n\n# Testing\nAfter installation, the test suite can be launched from outside the source directory ( although `pytest `>= 5.01 must be installed)\n```\npytest whitebeam \n```\n',
    'author': 'K-Molloy',
    'author_email': 'kieran.b.molloy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/K-Molloy/whitebeam',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
