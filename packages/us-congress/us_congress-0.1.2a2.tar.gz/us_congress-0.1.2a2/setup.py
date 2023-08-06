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
    'version': '0.1.2a2',
    'description': 'Client to work with US Congress data',
    'long_description': '[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n![Release](https://github.com/drawjk705/us-congress/workflows/Release/badge.svg)\n![CI](https://github.com/drawjk705/us-congress/workflows/CI/badge.svg)\n\n# US Congress\n\nClient for getting information on the US Congress.\n\n## Requirements\n\nFor this package to work, you must [get an API key from ProPublica](https://www.propublica.org/datastore/api/propublica-congress-api), whose API this uses, and set the following the environment variable `PROPUBLICA_CONG_KEY` to whatever that key is, either with\n\n```bash\nexport PROPUBLICA_CONG_KEY=<your key>\n```\n\nor in a `.env` file:\n\n```bash\nPROPUBLICA_CONG_KEY=<your key>\n```\n\n## Getting started\n\nTo install with pip, simply run\n\n```bash\npip install us_congress\n```\n\n```python\n>>> from us_congress import Congress\n>>> cong = Congress(116)\n>>> cong\n<Congress 116>\n```\n\nThis will return a client for querying data on a particular congress (in the above example, the 116th Congress).\n\nRight now, this enables only getting lists of Representatives and Senators:\n\n```python\ncong.getRepresentatives() # DataFrame with all representatives\ncong.getSenators()        # DataFrame with all senators\n```\n',
    'author': 'Joel Krim',
    'author_email': 'drawjk705@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/drawjk705/us-congress/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
