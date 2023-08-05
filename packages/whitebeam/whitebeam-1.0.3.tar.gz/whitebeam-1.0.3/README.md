# whitebeam

| | |
|---------|---|
| docs    | [![Documentation Status](https://readthedocs.org/projects/whitebeam/badge/?version=latest)](https://whitebeam.readthedocs.io/en/latest/?badge=latest) |
| test    | [![Build Status](https://travis-ci.com/K-Molloy/whitebeam.svg?branch=main)](https://travis-ci.com/K-Molloy/whitebeam) [![Requirements Status](https://requires.io/github/K-Molloy/whitebeam/requirements.svg?branch=main)](https://requires.io/github/K-Molloy/whitebeam/requirements/?branch=main)  |
| package | [![PythonVersion](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue)  [![PyPI version](https://badge.fury.io/py/Whitebeam.svg)](https://badge.fury.io/py/Whitebeam) ![GitHub commits since latest release (by date)](https://img.shields.io/github/commits-since/K-Molloy/whitebeam/latest) ![GitHub last commit](https://img.shields.io/github/last-commit/K-Molloy/whitebeam) [![codecov](https://codecov.io/gh/K-Molloy/whitebeam/branch/main/graph/badge.svg?token=KQDZUPH74N)](https://codecov.io/gh/K-Molloy/whitebeam)|

**whitebeam** is a python module for decision trees without the use of sklearn and SciPy

The project was started in 2020 by Kieran Molloy as a coursework component for SCC461 at Lancaster University

# Installation

## Dependencies

whitebeam requires:

- Python (>= 3.6)
- NumPy (>= 1.14)
- Cython (>= 0.29.21)
- joblib (>= 1.0.0)

## User Installation

If you already have a working directory, the easiest installation is via `pip`

```
pip install whitebeam
```

However it is advisable to install within a virtual environment

```
virtualenv venv
venv/bin/activate
pip install whitebeam
```

There will soon be more detailed installation instructions in the docs.

# Changelog

See the changelog for a history of notable changes to whitebeam

# Development

Development is planned to be ongoing however this may change due to university requirements.

## Source Installation

Installing from source requires `python-dev` which can be installed using 
```
sudo apt-get install python3-dev
```
then cloning this repo, installing requirements and building
```
git clone https://github.com/K-Molloy/whitebeam
pip install -r requirements.txt
python setup.py build_ext --inplace
```
again, it is advisable to use a virtual environment.

# Testing
After installation, the test suite can be launched from outside the source directory ( although `pytest `>= 5.01 must be installed)
```
pytest whitebeam 
```
