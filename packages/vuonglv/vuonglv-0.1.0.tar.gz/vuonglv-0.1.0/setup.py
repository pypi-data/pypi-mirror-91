# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vuonglv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vuonglv',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'vuonglv',
    'author_email': 'it.vuonglv@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
