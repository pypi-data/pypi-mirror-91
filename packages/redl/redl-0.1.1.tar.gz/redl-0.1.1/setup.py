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
    'version': '0.1.1',
    'description': 'A cli to download reddit video along with audio',
    'long_description': '# redl - A Reddit video downloader(with audio)\n\n\n### ⚠️ Requires `ffmpeg` installed\n\n\nRedl scrapes the reddit post json and retrives both audio and video URLs. Once these files are downloaded, it uses `ffmpeg` to join them. \n\n### Installation\n\n```bash\npip install redl --user\n```\n\n### Usage\n\n```bash\nredl https://www.reddit.com/r/Damnthatsinteresting/comments/kwrbde/making_a_grapefruit_dessert/\n```\n\n',
    'author': 'Amal Shaji',
    'author_email': 'amalshajid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/amalshaji/redl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
