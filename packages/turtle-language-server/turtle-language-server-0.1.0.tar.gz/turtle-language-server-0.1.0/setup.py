# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turtle_language_server']

package_data = \
{'': ['*']}

install_requires = \
['pygls>=0.9.1,<0.10.0', 'rdflib>=5.0.0,<6.0.0']

entry_points = \
{'console_scripts': ['turtle_langserver = turtle_language_server.entry:main']}

setup_kwargs = {
    'name': 'turtle-language-server',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
