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
    'version': '0.1.0',
    'description': 'Dead-simple parallel execution.',
    'long_description': None,
    'author': 'malyvsen',
    'author_email': '5940672+malyvsen@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
