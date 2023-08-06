# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polyomino']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover==0.3.2a2']

entry_points = \
{'console_scripts': ['doctest = build:run_doctests', 'test = build:run_tests']}

setup_kwargs = {
    'name': 'polyomino',
    'version': '0.2.0a0',
    'description': 'Solve polyomino tiling problems.',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
