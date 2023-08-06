# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hotair', 'hotair.template']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.6.0,<0.7.0',
 'lxml>=4.6.2,<5.0.0',
 'starlette>=0.14.1,<0.15.0',
 'uvicorn[standard]>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'hotair',
    'version': '0.1.0',
    'description': 'HTML Over The Air. Transporting HTML through WebSocket. Inspired by Hotwire.',
    'long_description': '# HTML Over The Air\n',
    'author': 'NCPlayz',
    'author_email': 'chowdhurynadir0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/serviper/hotair',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
