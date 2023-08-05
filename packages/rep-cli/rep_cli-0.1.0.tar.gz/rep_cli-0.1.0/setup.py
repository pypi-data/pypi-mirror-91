# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rep_cli']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.1,<2.0.0',
 'shellingham>=1.3.2,<2.0.0',
 'tabulate>=0.8.7,<0.9.0',
 'tinydb-serialization>=2.0.0,<3.0.0',
 'tinydb>=4.2.0,<5.0.0',
 'typer>=0.3.2,<0.4.0',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['rep = rep_cli.main:app']}

setup_kwargs = {
    'name': 'rep-cli',
    'version': '0.1.0',
    'description': 'A tiny tool for freelancers and contractors for tracking time and calculating invoices.',
    'long_description': None,
    'author': 'Wojciech Bogócki',
    'author_email': 'wojciechbogocki@fastmail.com',
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
