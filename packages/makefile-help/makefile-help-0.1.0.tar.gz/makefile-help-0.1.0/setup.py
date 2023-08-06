# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['makefile_help']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['makefile-help = makefile_help.__main__:main']}

setup_kwargs = {
    'name': 'makefile-help',
    'version': '0.1.0',
    'description': 'Autogenerates pretty Makefile help',
    'long_description': '# Makefile help\n\nThis small package helps by generating colourful help for Makefiles.\n- [Makefile help](#makefile-help)\n    - [Why?](#why)\n    - [Usage](#usage)\n    - [Installation](#installation)\n\n---\n### Why?\n\nI often store useful commands in Makefiles and then promptly forget them.\n\n---\n### Usage\n\nAt the top of a Makefile add the following (assuming makefile-help is installed in the current virtual env):\n\n```\nhelp: # @@Utils@@ Display help and exit\n\tpython -m makefile_help\n```\n\nComment each command with a description and optionally a section using `@@`  \nThe makefile_help script will then generate a help string.\n\n![](../makefile-help/image/demo.gif)\n\n---\n### Installation\n\n`pip install makefile-help`',
    'author': 'simonwardjones',
    'author_email': 'simonwardjones@yahoo.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonwardjones/makefile-help',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
