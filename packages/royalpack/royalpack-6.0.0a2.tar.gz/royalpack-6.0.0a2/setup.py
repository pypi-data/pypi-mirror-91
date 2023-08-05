# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalpack', 'royalpack.commands']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'coloredlogs>=15.0,<16.0',
 'royalnet>=6.0.0a36,<7.0.0']

setup_kwargs = {
    'name': 'royalpack',
    'version': '6.0.0a2',
    'description': 'Royalnet Commands for the RYG community',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'ste.pigozzi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
