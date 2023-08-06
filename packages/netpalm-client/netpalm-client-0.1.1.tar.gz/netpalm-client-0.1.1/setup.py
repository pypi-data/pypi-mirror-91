# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netpalm_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'netpalm-client',
    'version': '0.1.1',
    'description': 'Simple Client for accessing a Netpalm Service',
    'long_description': '',
    'author': 'Will George',
    'author_email': 'wrgeorge1983@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
