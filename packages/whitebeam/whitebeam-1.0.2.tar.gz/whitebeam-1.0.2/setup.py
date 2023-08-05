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
    'version': '1.0.2',
    'description': 'Whitebeam is a framework for creating decision tree functions.',
    'long_description': None,
    'author': 'K-Molloy',
    'author_email': 'kieran.b.molloy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
