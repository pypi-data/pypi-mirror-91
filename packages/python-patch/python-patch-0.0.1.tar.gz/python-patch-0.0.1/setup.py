# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['patch']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-patch',
    'version': '0.0.1',
    'description': 'Make your python smart',
    'long_description': '## Make your python smart\n\n',
    'author': 'Denis Kayshev',
    'author_email': 'topenkoff@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/topenkoff/python-patch',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
