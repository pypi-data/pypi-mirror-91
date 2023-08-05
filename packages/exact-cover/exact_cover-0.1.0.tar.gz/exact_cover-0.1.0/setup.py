# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exact_cover']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.4,<2.0.0']

entry_points = \
{'console_scripts': ['test = build:test']}

setup_kwargs = {
    'name': 'exact-cover',
    'version': '0.1.0',
    'description': 'Solve exact cover problems',
    'long_description': None,
    'author': 'Moy Easwaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
