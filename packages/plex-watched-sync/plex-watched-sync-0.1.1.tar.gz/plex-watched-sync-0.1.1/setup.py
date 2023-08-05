# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plex_watched_sync']

package_data = \
{'': ['*']}

install_requires = \
['PlexAPI>=4.2.0,<5.0.0',
 'click>=7.1.2,<8.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

entry_points = \
{'console_scripts': ['plex-watched-sync = plex_watched_sync.cli:main']}

setup_kwargs = {
    'name': 'plex-watched-sync',
    'version': '0.1.1',
    'description': 'Small tool to synchronize watched status from one Plex server to another',
    'long_description': '# plex-watched-sync\n\n*plex-watched-sync* is a small tool which helps you synchronize\nthe watched status of items on one Plex server to another Plex server.\n\nThe target is to provide a tool which can be used to synchronize watched\nstatus information when copying contents to a new Plex instance.\n\n## Usage\n\n```bash\npip3 install plex-watched-sync\nplex-watched-sync\n```\n\n**or**\n\n```bash\ngit clone https://github.com/speijnik/plex-watched-sync.git\ncd plex-watched-sync\npoetry install\npoetry run plex-watched-sync\n```\n',
    'author': 'Stephan Peijnik-Steinwender',
    'author_email': 'speijnik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/speijnik/plex-watched-sync',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
