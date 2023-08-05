# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['winbotswppi', 'winbotswppi.webwhatsapi', 'winbotswppi.webwhatsapi.objects']

package_data = \
{'': ['*'], 'winbotswppi.webwhatsapi': ['js/*']}

setup_kwargs = {
    'name': 'winbotswppi',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Winbots',
    'author_email': 'jorgebg2016@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
