# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manydo']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.0.0,<2.0.0', 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'manydo',
    'version': '0.1.1',
    'description': 'Dead-simple parallel execution.',
    'long_description': '# manydo\nDead-simple parallel execution.\n\n## Installation\n`pip install manydo`. Or, better for you, use [Poetry](python-poetry.org/): `poetry add manydo`.\n\n## Usage\n`manydo` is simple. All you need is `map`:\n```python\nfrom manydo import map\n\nmap(lambda x: x + 3, [1, 2, 3]) # [4, 5, 6]\nmap(function, iterable, num_jobs=16) # try not to burn your CPU\nmap(function, iterable, loading_bar=False) # if you insist\n```\n',
    'author': 'malyvsen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/malyvsen/manydo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
