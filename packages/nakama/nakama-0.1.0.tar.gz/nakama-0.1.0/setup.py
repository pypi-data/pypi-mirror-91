# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nakama']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'nakama',
    'version': '0.1.0',
    'description': 'Python client for nakama server',
    'long_description': None,
    'author': 'Felipe Ruhland',
    'author_email': 'felipe.ruhland@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
