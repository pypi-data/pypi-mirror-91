# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aopi_index_builder']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'SQLAlchemy>=1.3.22,<2.0.0',
 'databases>=0.4.1,<0.5.0',
 'entrypoints>=0.3,<0.4',
 'fastapi>=0.63.0,<0.64.0',
 'loguru>=0.5.3,<0.6.0',
 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'aopi-index-builder',
    'version': '0.1.41',
    'description': 'Package to build new package indices for AOPI',
    'long_description': None,
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': 'Pavel Kirilin',
    'maintainer_email': 'win10@list.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
