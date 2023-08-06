# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygennaro']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['pygennaro = pygennaro.commandline:command_line_handler']}

setup_kwargs = {
    'name': 'pygennaro',
    'version': '0.1.0',
    'description': 'BNF parsing, formal grammar conversion and string generation utilities',
    'long_description': None,
    'author': 'Kien Tuong Truong',
    'author_email': 'info@ktruong.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
