# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stream_csv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stream-csv',
    'version': '0.1.1',
    'description': 'Ways to stream CSV content.',
    'long_description': '<h1 align="center">\n    <strong>stream-csv</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/stream-csv" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/stream-csv" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/stream-csv/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/stream-csv">\n    <br />\n    <a href="https://pypi.org/project/stream-csv" target="_blank">\n        <img src="https://img.shields.io/pypi/v/stream-csv" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/stream-csv">\n    <img src="https://img.shields.io/github/license/Kludex/stream-csv">\n</p>\n\n\n## Installation\n\n``` bash\npip install stream-csv\n```\n\n## Usage\n\n```python\nfrom fastapi import FastAPI\nfrom starlette.responses import StreamingResponse\n\nfrom stream_csv.stream import stream_data\n\napp = FastAPI()\n\n\n@app.get("/")\ndef get_csv():\n    headers = ["type", "color", "size"]\n    dict_data = [\n        {"type": "potato", "color": "blue", "size": 1},\n        {"type": "banana", "color": "red", "size": 2},\n        {"type": "potato", "size": 3, "color": "yellow"},\n    ]\n    return StreamingResponse(\n        stream_data(dict_data, headers),\n        media_type="text/csv",\n        headers={"Content-Disposition": "attachment; filename=data.csv"},\n    )\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
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
