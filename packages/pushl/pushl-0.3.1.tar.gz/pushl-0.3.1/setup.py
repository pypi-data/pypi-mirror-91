# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pushl']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.3,<4.0.0',
 'async_lru>=1.0.2,<2.0.0',
 'awesome-slugify>=1.6.5,<2.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'feedparser>=6.0.2,<7.0.0',
 'lxml>=4.6.2,<5.0.0',
 'mf2py>=1.1.2,<2.0.0']

entry_points = \
{'console_scripts': ['pushl = pushl.__main__:main']}

setup_kwargs = {
    'name': 'pushl',
    'version': '0.3.1',
    'description': 'A conduit for pushing changes in a feed to the rest of the IndieWeb',
    'long_description': None,
    'author': 'fluffy',
    'author_email': 'fluffy@beesbuzz.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
