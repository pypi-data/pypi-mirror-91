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
    'version': '0.1.2',
    'description': 'A tiny tool for freelancers and contractors for tracking time and calculating invoices.',
    'long_description': "![Logo](https://raw.githubusercontent.com/wbogocki/Rep/master/logo.svg)\n\n[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/license-MIT-blueviolet.svg)](LICENSE.txt)\n\nRep is a tiny tool for freelancers and contractors to track time and calculate invoices. It's written primarily based on my experience and process so it definitely won't work for all of you out there. However, some of you might still find it useful.\n\nAt the moment, Rep can:\n\n-   Track time\n-   Take notes\n-   Calculate invoices\n\n## Approach\n\nRep uses logs to track time and group notes. It's a very simple approach that I used to use with pen and paper.\n\nFor example, this is a single log:\n\n```\nNov 4 2020 14:00 - Start work\nNov 4 2020 18:00 - Note: Let's go, wohoooooo!\nNov 5 2020 00:30 - Stop work\n```\n\nRep stores these logs inside a hidden `.rep` directory in your project folder. The database is a human-friendly JSON file that can be manually edited when needed.\n\n## Usage\n\nThere are six commands you need to know to use Rep:\n\n| Command       | Action                                         |\n| ------------- | ---------------------------------------------- |\n| `rep init`    | Initialize Rep in the current directory.       |\n| `rep start`   | Open a new log and start measuring time.       |\n| `rep stop`    | Close the current log and stop measuring time. |\n| `rep note`    | Add a note to the last log.                    |\n| `rep table`   | Print logs in a table (doesn't show notes).    |\n| `rep print`   | Print logs and notes.                          |\n| `rep invoice` | Print the invoice amount for unbilled logs.    |\n| `rep bill`    | Mark logs as billed.                           |\n\n## License\n\nRep is licensed under the MIT license.\n",
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
