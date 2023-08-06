# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['column_diff']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.5,<4.0.0', 'pandas>=1.1.4,<2.0.0', 'xlrd>=1.2.0,<2.0.0']

setup_kwargs = {
    'name': 'column-diff',
    'version': '0.1.1',
    'description': 'A Python package to filter emails from two columns of an Excel spreadsheet.',
    'long_description': 'Description\n===========\n\nA Python package to filter emails from two columns of an Excel spreadsheet.\n\n\nInstallation\n============\n\n.. code-block::\n\n    pip install column-diff\n\nExample Usage\n=============\n.. code-block:: python\n\n    filter_file("input.xlsx")\n    filter_file("input.xlsx", blacklist_column=3)\n\n',
    'author': 'Thomas Breydo',
    'author_email': 'tbreydo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
