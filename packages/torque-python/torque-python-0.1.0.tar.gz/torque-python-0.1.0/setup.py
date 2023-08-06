# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torque_python']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'torque-python',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Torque, Inc.',
    'author_email': 'development@torque.cloud',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
