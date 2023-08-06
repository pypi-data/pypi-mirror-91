# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_test_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-test-test',
    'version': '0.1.3',
    'description': 'This is an amazing description',
    'long_description': '# This is a pretty cool description!',
    'author': 'amitkummer',
    'author_email': 'amit.kummer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
