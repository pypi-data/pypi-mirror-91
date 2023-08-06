# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['invisible_di']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'invisible-di',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lasse Enø Barslund',
    'author_email': 'lasse_enoe@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
