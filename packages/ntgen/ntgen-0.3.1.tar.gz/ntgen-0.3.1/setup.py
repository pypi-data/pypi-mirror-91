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
    'version': '0.3.1',
    'description': 'named tuple generator',
    'long_description': '# ntgen - named tuple generator\n[![CircleCI](https://img.shields.io/circleci/build/github/mrapacz/ntgen)](https://circleci.com/gh/mrapacz/ntgen)\n[![PyPI - Package Version](https://img.shields.io/pypi/v/ntgen)](https://pypi.org/project/ntgen/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ntgen.svg)](https://pypi.org/project/ntgen/)\n[![Coverage Status](https://coveralls.io/repos/github/mrapacz/ntgen/badge.svg?branch=master)](https://coveralls.io/github/mrapacz/ntgen?branch=master)\n[![PyPI - License](https://img.shields.io/pypi/l/ntgen)](LICENSE)\n\nGenerate NamedTuple definitions with typehints based on your data automatically.\nIf you\'ve ever felt like preparing NamedTuple skeletons for any json data you\'re dealing with is tedious and could be\nautomated, well, this is the tool that automates the process.\n\n## Usage\nLet\'s say you want to prepare a NamedTuple definition for the following json object:\n```bash\n$ cat apartment.json\n{\n    "id": "1234-1234",\n    "type": "living",\n    "isAvailable": true,\n    "countryCode": "DE",\n    "address": {\n        "borough": "Dulsberg",\n        "city": "Hamburg",\n        "houseNumber": "2",\n        "latitude": 53.587485,\n        "longitude": 10.063215,\n        "postalCode": "22049",\n        "streetName": "Nordschleswiger Strasse",\n        "area": "Hamburg"\n    },\n    "_attachments": "attachments/",\n    "_ts": 15828103462\n}%\n```\n\nAll you need to do is run the following command:\n```bash\n$ ntgen apartment.json\nclass Address(NamedTuple):\n    borough: str\n    city: str\n    house_number: str\n    latitude: float\n    longitude: float\n    postal_code: str\n    street_name: str\n    area: str\n\n\nclass Apartment(NamedTuple):\n    id: str\n    type: str\n    is_available: bool\n    country_code: str\n    address: Address\n    attachments: str\n    ts: int\n\n```\nThe output will be directed to stdout by default - you may also redirect it to a file to bootstrap a Python module with\nthe class definitions.\n\n## Runtime configuration\n\nTo find out about all of the runtime configuration options, run:\n```bash\n$ ntgen --help\nusage: ntgen [--out OUT] [--name NAME] [-s] [-c] [-f] [-t]\n             [--max_level MAX_LEVEL] [-h]\n             input\n\npositional arguments:\n  input                 (str, default=None) Json file containing an object\n                        with the data to analyzed\n\noptional arguments:\n  --out OUT             (Union[str, NoneType], default=None) Destination file\n                        to write the Python code to\n  --name NAME           (str, default=NTGenTuple) Name of the main NamedTuple\n  -s, --snake-case      (bool, default=True) Convert the NamedTuple field\n                        names to snake_case\n  -c, --camel-case      (bool, default=True) Convert the NamedTuple class\n                        names to CamelCase\n  -f, --constructors    (bool, default=False) Insert generic methods that will\n                        allow for parsing of the analyzed data structures\n  -t, --as-dict         (bool, default=False) Insert generic methods allowing\n                        for dumping the nested NamedTuple hierarchy to a dict\n  --max_level MAX_LEVEL\n                        (Union[int, NoneType], default=None) Specify the max\n                        nesting level of the NamedTuple\n  -h, --help            show this help message and exit\n```\n\n## Other invocation options\nYou can also use the library from the Python context:\n```python\n>>> from ntgen import generate_from_dict\n>>> data = {\'name\': \'John Wick\', \'profession\': \'assassin\', \'age\': 34}\n>>> print(generate_from_dict(data=data, name="Character"))\nclass Character(NamedTuple):\n    name: str\n    profession: str\n    age: int\n\n```\n## Installation\nYou\'ll need to be running Python >= 3.7.\n```bash\npip install ntgen\n```\nVerify that the latest package version was installed correctly:\n```python\n>>> import ntgen\n>>> ntgen.__version__\n\'0.3.0\'\n\n```\n\n## License\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n## Author\nMaciej Rapacz\n',
    'author': 'Maciej Rapacz',
    'author_email': 'mmrapacz@protonmail.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
