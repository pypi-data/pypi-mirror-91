# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['us_congress',
 'us_congress._api',
 'us_congress._members',
 'us_congress._transformation',
 'us_congress._utils',
 'us_congress._utils.log']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.0,<2.0.0',
 'punq>=0.4.1,<0.5.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'us>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'us-congress',
    'version': '0.1.2a0',
    'description': 'Client to work with US Congress data',
    'long_description': None,
    'author': 'Joel Krim',
    'author_email': 'drawjk705@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
