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
    'version': '0.1.2',
    'description': 'Unofficial CLI tool to display power outages in Perth',
    'long_description': '# ungoliant: unofficial CLI tool to list Perth power outages\n\nMakes use of Western Power data.\n\n## Installation\n\n```bash\npoetry install\n```\n\nExample output:\n\n```\n         Started | Est. Restoration | Cust. | Affected areas\n-----------------|------------------|-------|-----------------------------------\n2021-01-14 08:13 | 2021-01-14 16:30 |   297 | GERALDTON,MOUNT TARCOOLA\n2021-01-14 08:04 | 2021-01-14 18:30 |   575 | BEDFORDALE,ROLEYSTONE\n2021-01-04 08:25 | 2021-01-14 19:00 |     1 | MALLEE HILL\n2021-01-14 13:56 | 2021-01-14 16:30 |    43 | DAYTON\n2021-01-14 10:26 | 2021-01-14 18:30 |   123 | DAWESVILLE,BOUVARD\n2021-01-14 11:17 | 2021-01-14 17:00 |    28 | MILO,MOORIARY,MOUNT ADAMS,YARDARINO\n2021-01-14 14:57 | 2021-01-14 17:30 |     6 | HARVEY\n2021-01-14 13:34 | 2021-01-14 23:30 |   362 | BAYSWATER,EMBLETON\n2021-01-14 00:08 | 2021-01-14 21:04 |    68 | GIDGEGANNUP,BRIGADOON\n\nPlease note: This tool is unoffical.\n```\n',
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
