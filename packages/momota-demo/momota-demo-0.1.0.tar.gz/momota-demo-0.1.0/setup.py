# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['momota_demo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'momota-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Momota Sasaki',
    'author_email': 'momota.sasaki@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
