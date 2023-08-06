# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jeejuh_dl']

package_data = \
{'': ['*']}

install_requires = \
['gazpacho>=1.1,<2.0', 'rich>=9.8.2,<10.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['jeejuh-dl = jeejuh_dl.main:app']}

setup_kwargs = {
    'name': 'jeejuh-dl',
    'version': '1.0.0',
    'description': 'Downloads links from jeejuh.com purchases',
    'long_description': None,
    'author': 'Leron Gray',
    'author_email': None,
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
