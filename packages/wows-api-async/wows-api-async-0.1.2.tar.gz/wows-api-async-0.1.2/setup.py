# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wows_api_async', 'wows_api_async.cache', 'wows_api_async.nodes']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'httpx>=0.16.1,<0.17.0', 'pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'wows-api-async',
    'version': '0.1.2',
    'description': 'async python api for world of warships',
    'long_description': None,
    'author': 'Lajos Santa',
    'author_email': 'santa.lajos@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/voidpp/wows-api-async',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
