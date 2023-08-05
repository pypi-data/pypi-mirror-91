# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_console']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'royalnet>=6.0.0a36,<7.0.0']

setup_kwargs = {
    'name': 'royalnet-console',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Stefano Pigozzi',
    'author_email': 'me@steffo.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
