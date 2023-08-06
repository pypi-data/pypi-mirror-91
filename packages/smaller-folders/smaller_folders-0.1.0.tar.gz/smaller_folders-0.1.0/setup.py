# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['smaller_folders']

package_data = \
{'': ['*']}

install_requires = \
['more-itertools>=8.6.0,<9.0.0', 'natsort>=7.1.0,<8.0.0']

entry_points = \
{'console_scripts': ['smaller_folders = smaller_folders.cli:main']}

setup_kwargs = {
    'name': 'smaller-folders',
    'version': '0.1.0',
    'description': 'Split an arbitrary number of files into sub-folders containing a specified number of files each.',
    'long_description': None,
    'author': 'Aatif Syed',
    'author_email': 'aatif@aatifsyed.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
