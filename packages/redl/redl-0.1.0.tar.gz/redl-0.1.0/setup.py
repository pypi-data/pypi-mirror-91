# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['redl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'tqdm>=4.56.0,<5.0.0']

entry_points = \
{'console_scripts': ['redl = redl.main:main']}

setup_kwargs = {
    'name': 'redl',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Amal Shaji',
    'author_email': 'amalshajid@gmail.com',
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
