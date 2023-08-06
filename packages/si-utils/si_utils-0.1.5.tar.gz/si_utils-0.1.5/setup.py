# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['si_utils', 'si_utils._vendor', 'si_utils._vendor.boltons']

package_data = \
{'': ['*']}

extras_require = \
{'dev-utils': ['tomlkit>=0.7.0,<0.8.0', 'semver>=2.13.0,<3.0.0'],
 'log': ['loguru>=0.5,<0.6', 'sentry-sdk>=0.19,<0.20'],
 'yaml': ['ruamel.yaml>=0.16,<0.17', 'deepmerge>=0.1,<0.2', 'pydantic>=1,<2']}

setup_kwargs = {
    'name': 'si-utils',
    'version': '0.1.5',
    'description': 'an opinionated set of utilities designed to be easily included in any number of projects',
    'long_description': None,
    'author': 'Alex Tremblay',
    'author_email': 'alex.tremblay@utoronto.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
