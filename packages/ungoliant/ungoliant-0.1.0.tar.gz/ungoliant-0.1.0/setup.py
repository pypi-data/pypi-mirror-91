# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ungoliant']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

entry_points = \
{'console_scripts': ['ungoliant = ungoliant.cli:main']}

setup_kwargs = {
    'name': 'ungoliant',
    'version': '0.1.0',
    'description': 'Unofficial CLI tool to display power outages in Perth',
    'long_description': None,
    'author': 'Grahame Bowland',
    'author_email': 'grahame@oreamnos.com.au',
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
