# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['whois_vu']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'whois-vu',
    'version': '0.1.0',
    'description': 'Synchronous python wrapper for api.whois.vu',
    'long_description': None,
    'author': 'kiriharu',
    'author_email': 'kiriharu@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
