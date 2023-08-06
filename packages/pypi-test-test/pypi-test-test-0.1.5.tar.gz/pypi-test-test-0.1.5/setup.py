# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pypi_test_test']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pypi-test-test',
    'version': '0.1.5',
    'description': 'This is an amazing description',
    'long_description': '# This is a pretty cool description!\n\n\n1. Installing the pacakge:\n\n    ```sh\n    $ pip install this-cool-package\n    ```\n\n2. Removeing the package:\n\n    ```sh\n    pip remove this-cool-package\n    ```',
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
