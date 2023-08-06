# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['caapi_shared']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.3,<2.0.0']

setup_kwargs = {
    'name': 'caapi-shared',
    'version': '1.0.3',
    'description': 'Shared library for all services that are part of the VA-administered Claims Attributes API',
    'long_description': None,
    'author': 'Nat Hillard',
    'author_email': 'nathaniel.hillard@va.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
