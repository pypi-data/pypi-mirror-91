# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['msucom_qbank']

package_data = \
{'': ['*'],
 'msucom_qbank': ['data/*',
                  'static/*',
                  'templates/*',
                  'templates/auth/*',
                  'templates/quiz/*']}

install_requires = \
['Flask>=1.1.2,<2.0.0', 'gunicorn>=20.0.4,<21.0.0', 'loguru>=0.5.3,<0.6.0']

setup_kwargs = {
    'name': 'msucom-qbank',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'BGASM',
    'author_email': 'slatte26@msu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
