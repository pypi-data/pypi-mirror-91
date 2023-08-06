# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ntgen']

package_data = \
{'': ['*']}

install_requires = \
['pyannotate>=1.2.0,<2.0.0']

entry_points = \
{'console_scripts': ['ntgen = ntgen.__main__:console_entry']}

setup_kwargs = {
    'name': 'ntgen',
    'version': '0.3.0',
    'description': 'named tuple generator',
    'long_description': None,
    'author': 'Maciej Rapacz',
    'author_email': 'mmrapacz@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
