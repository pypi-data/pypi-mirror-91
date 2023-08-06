# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['polybar_clockify']

package_data = \
{'': ['*']}

install_requires = \
['isodate>=0.6.0,<0.7.0', 'requests>=2.25.1,<3.0.0', 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['polybar-clockify = polybar_clockify.app:run']}

setup_kwargs = {
    'name': 'polybar-clockify',
    'version': '0.1.0',
    'description': 'Quick access to control clockify through polybar',
    'long_description': 'polybar-clockify\n================\nIntegrates polybar with clockify\n\nConfigure\n---------\nCreate a ``credentials.json`` in the root directory with your clockify API key.\n\n::\n\n    {\n      "api-key": "your-api-key",\n      "email": "your-email",\n      "password": "your-password"\n    }\n',
    'author': 'Wout De Puysseleir',
    'author_email': 'woutdp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/woutdp/polybar-clockify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
