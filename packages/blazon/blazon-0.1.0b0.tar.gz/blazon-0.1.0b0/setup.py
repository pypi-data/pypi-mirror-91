# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['blazon', 'blazon.constraints', 'blazon.environments']

package_data = \
{'': ['*']}

install_requires = \
['inflection>=0.3.1,<0.4.0', 'shortuuid>=1.0.1,<2.0.0']

setup_kwargs = {
    'name': 'blazon',
    'version': '0.1.0b0',
    'description': 'A library for assuring data structure and format, with tools for mapping to objects, and multi-schema system translation.',
    'long_description': None,
    'author': 'Brantley Harris',
    'author_email': 'deadwisdom@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/deadwisdom/blazon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
