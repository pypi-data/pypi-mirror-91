# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['codefellows', 'codefellows.dsa']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'codefellows',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'codefellows',
    'author_email': 'jb@codefellows.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
