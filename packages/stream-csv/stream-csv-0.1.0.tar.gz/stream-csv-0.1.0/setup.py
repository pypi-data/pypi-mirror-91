# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stream_csv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stream-csv',
    'version': '0.1.0',
    'description': 'Ways to stream CSV content.',
    'long_description': '<h1 align="center">\n    <strong>stream-csv</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/stream-csv" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/stream-csv" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/stream-csv/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/stream-csv">\n    <br />\n    <a href="https://pypi.org/project/stream-csv" target="_blank">\n        <img src="https://img.shields.io/pypi/v/stream-csv" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/stream-csv">\n    <img src="https://img.shields.io/github/license/Kludex/stream-csv">\n</p>\n\n\n## Installation\n\n``` bash\npip install stream-csv\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/stream-csv',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
