# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_repo_move']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['git-repo-move = git_repo_move.cli:main']}

setup_kwargs = {
    'name': 'git-repo-move',
    'version': '1.0.0',
    'description': 'Move files from one git repo to another, preserving history',
    'long_description': None,
    'author': 'Alan Rosenthal',
    'author_email': '1288897+AlanRosenthal@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
