# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['schema_builder']

package_data = \
{'': ['*']}

install_requires = \
['autopep8>=1.5.4,<2.0.0', 'pylint>=2.6.0,<3.0.0', 'pytest-cov>=2.10.1,<3.0.0']

setup_kwargs = {
    'name': 'schema-builder',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Michael Cooper',
    'author_email': 'macoop2363@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
