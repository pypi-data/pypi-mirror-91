# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['windows_ha_util']

package_data = \
{'': ['*']}

install_requires = \
['python-nmap>=0.6.1,<0.7.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'windows-ha-util',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jacob Clarke',
    'author_email': 'jacobclarke718@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
