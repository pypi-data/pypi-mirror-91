# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['kuro2sudachi']

package_data = \
{'': ['*']}

install_requires = \
['jaconv>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['kuro2sudachi = kuro2sudachi.core:cli']}

setup_kwargs = {
    'name': 'kuro2sudachi',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'po3rin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
