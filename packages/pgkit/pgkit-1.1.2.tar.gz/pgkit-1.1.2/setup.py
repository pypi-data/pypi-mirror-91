# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pgkit',
 'pgkit.application',
 'pgkit.application.templates',
 'pgkit.cli',
 'pgkit.cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'click>=7.1.2,<8.0.0', 'tinydb>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'pgkit',
    'version': '1.1.2',
    'description': '',
    'long_description': None,
    'author': 'Sadegh Hayeri',
    'author_email': 'hayerisadegh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
