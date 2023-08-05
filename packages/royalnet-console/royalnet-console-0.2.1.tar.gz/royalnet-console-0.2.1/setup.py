# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['royalnet_console', 'royalnet_console.utils']

package_data = \
{'': ['*']}

install_requires = \
['psutil>=5.8.0,<6.0.0', 'royalnet>=6.0.0a37,<7.0.0']

setup_kwargs = {
    'name': 'royalnet-console',
    'version': '0.2.1',
    'description': 'A terminal-based frontend for the royalnet.engineer module.',
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
