# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aopi_python',
 'aopi_python.models',
 'aopi_python.routes',
 'aopi_python.routes.simple',
 'aopi_python.utils']

package_data = \
{'': ['*'], 'aopi_python': ['templates/simple/*']}

install_requires = \
['aiofile>=3.3.3,<4.0.0',
 'aopi-index-builder>=0.1.40,<0.2.0',
 'loguru>=0.5.3,<0.6.0',
 'natsort>=7.1.0,<8.0.0',
 'orm>=0.1.5,<0.2.0',
 'ujson>=4.0.1,<5.0.0']

entry_points = \
{'aopi_index': ['python = aopi_python.main:main']}

setup_kwargs = {
    'name': 'aopi-python',
    'version': '0.1.23',
    'description': '',
    'long_description': 'Python package index module.\n============================\n\nThis module adds python package index to your aopi server.',
    'author': 'Pavel Kirilin',
    'author_email': 'win10@list.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
