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
    'version': '1.0.3',
    'description': 'Simple Client for accessing a Netpalm Service',
    'long_description': "# Netpalm-Client\n\nSimple client library for working with [Netpalm](https://github.com/tbotnz/netpalm)\n\nDetailed example available in [examples](https://github.com/wrgeorge1983/netpalm-client/tree/master/example) folder of this repo\n\n\n## Install\n```\npip install netpalm-client\n```\n\n## Basic Usage\n```python\nfrom netpalm_client import NetpalmClient\n\nnetpalm = NetpalmClient(\n    url='https://netpalm.example.org',\n    key='someApiKey',\n    cli_user='cisco',\n    cli_pass='cisco'\n)\n\ntask_id = netpalm.netmiko_getconfig(\n    command='show run | i bgp router-id',\n    host='192.168.0.1'\n)['task_id']\n\nnetpalm_result = netpalm.poll_task(task_id)  # blocks until polling returns either completion or failure\n\nactual_result = netpalm_result['task_result'][command]  # failures will have a 'task_errors' key, but not a 'task_result' key.\n\nprint(f'{actual_result=}')\n```",
    'author': 'Will George',
    'author_email': 'wrgeorge1983@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wrgeorge1983/netpalm-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
