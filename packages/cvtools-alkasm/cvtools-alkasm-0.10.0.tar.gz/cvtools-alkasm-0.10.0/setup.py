# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cvtools', 'cvtools.extras']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python!=4.2.0.32']

setup_kwargs = {
    'name': 'cvtools-alkasm',
    'version': '0.10.0',
    'description': 'Utilities for computer vision in Python',
    'long_description': 'A collection of useful utilities for computer vision in Python. \n\n## Install\n    \n```sh\npip install cvtools-alkasm\n```\n',
    'author': 'Alexander Reynolds',
    'author_email': 'ar@reynoldsalexander.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alkasm/cvtools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
