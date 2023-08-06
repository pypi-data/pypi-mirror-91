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
    'version': '0.1.1',
    'description': 'Control Clockify through Polybar',
    'long_description': '================\npolybar-clockify\n================\n.. image:: https://badge.fury.io/py/polybar-clockify.svg\n    :target: https://badge.fury.io/py/polybar-clockify\n\nControl Clockify through Polybar\n\n\nInstallation\n------------\n::\n\n    pip install polybar-clockify\n\n\nConfiguration\n-------------\nCreate credentials file in ``~/.config/polybar/clockify/credentials.json`` and fill out your clockify credentials.\nYour will have to create a `clockify API key <https://clockify.me/user/settings/>`_ to make the module work. ::\n\n    {\n      "api-key": "your-api-key",\n      "email": "your-email",\n      "password": "your-password"\n    }\n\n\nCreate a polybar module inside your polybar config add it to your active modules. ::\n\n    [module/clockify]\n    type = custom/script\n    tail = true\n    exec = polybar-clockify\n    click-left = echo \'TOGGLE_TIMER\' | nc 127.0.0.1 30300\n    click-right = echo \'TOGGLE_HIDE\' | nc 127.0.0.1 30300\n\n\nDevelopment\n-----------\nThis package uses `poetry <https://python-poetry.org/>`_\n\n\nContribution\n------------\nAt the moment the functionality is pretty basic, but sufficient for my use case.\nIf you want to extend the functionality I\'d be delighted to accept pull requests!',
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
