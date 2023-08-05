# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfnsane', 'cfnsane.resources']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'toml>=0.10.2,<0.11.0', 'troposphere>=2.6.3,<3.0.0']

setup_kwargs = {
    'name': 'cfnsane',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Michael Neil',
    'author_email': 'mneil@mneilsworld.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
