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
    'version': '1.0.1',
    'description': 'Move files from one git repo to another, preserving history',
    'long_description': "# git-repo-move\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/AlanRosenthal/git-repo-move/build-ci?style=build-ci)](https://github.com/AlanRosenthal/git-repo-move)\n\nMove files from one git repo to another, preserving history!\nUnder the hood, this utility uses [`git filter-branch`](https://git-scm.com/docs/git-filter-branch), but the API is much more user friendly.\n\n## How-To\n\n### Install\n\n```sh\npip install git-repo-move\n```\n\n### Build Locally\n\n```sh\npoetry build\n```\n\n### Run It\n\nIf you've already installed in via `pip`, it's really easy to use.\nThe program is called `git-repo-move`.\nYou can also checkout the source and build locally by running:\n\n```sh\npoetry install --no-dev\n```\n\n#### Select Files and Directories\n\nSelect what files you want to keep by specifying:\n\n```sh\n--file path/to/file.txt --file path/to/another_file.txt\n```\n\nand what directories you want to keep by specifying:\n\n```sh\n--directory path/to/subfolder --directory path/to_another subfolder\n```\n\n#### Select the Final Directory for the Files\n\nOptionally, specify the final directory for the files\n\n```sh\n--final_directory newpath/to/thefiles\n```\n\n#### Select Directory Structure\n\nYou can either flatten all files or keep the original directory structure\n\n```sh\n--directory-structure <FLAT|ORIGINAL>\n```\n\nFor example:\n\n```sh\n--file path/to/file.txt --final-directory newpath/to/thefiles --directory-structure FLAT\n```\n\n`file.txt` will end up at `newpath/to/thefiles/flat.txt`\n\n```sh\n--file path/to/file.txt --final-directory newpath/to/thefiles --directory-structure ORIGINAL\n```\n\n`file.txt` will end up at `newpath/to/thefiles/path/to/file.txt`\n\n#### Specify the Git Remote URL of the Destination Repo\n\nYou can run `git remote -v` to get a list of remote URLs.\n\n```sh\n--git-remote-url git@github.com:AlanRosenthal/git-repo-move.git\n```\n\n#### Specify the Git Branch Name\n\nRemember this branch will used on both repos.\n\n```sh\n--git-branch move_files\n```\n\n#### Save Shell Script\n\nThis utility generates a shell script.\nBy default, the script will be saved in the root of the repo with the name `git-repo-move.sh`.\n\nYou can change the default name by specifying\n\n```sh\n--shell-script-name best-script-ever.sh\n```\n\nIt is recommended to include the generated shell script on your PR.\n\nOptionally, don't save a shell script by specifying the `--dont-save-shell-script` flag.\n\n\n#### Try It Out\n\nThis utility uses `git-filter-branch` which is relatively slow, especially for large repos.\nIt usually takes a few attempts to specify the correct files and directories.\n\nBy specifying the `--try-keep` flag, `git-repo-move` will move the specified files into a folder.\nInspect that folder to ensure everything is correct.\n\n#### Execute\n\nBy specifying the `--execute` flag, the generated script will be executed.\n\n### Example\n\nWe're using [`click`](https://github.com/pallets/click/) for the example.\n\nWe want to save [`src/click/formatting.py`](https://github.com/pallets/click/blame/2fc486c880eda9fdb746ed8baa49416acab9ea6d/src/click/formatting.py) and [`src/click/parser.py`](https://github.com/pallets/click/blame/2fc486c880eda9fdb746ed8baa49416acab9ea6d/src/click/parser.py) and have them end up in the folder `alan/click`.\n\nRunning the command:\n\n```sh\ngit-repo-move --file click/formatting.py --file src/click/formatting.py --file click/parser.py --file src/click/parser.py --final_directory alan/click --directory-structure flat --git-remote-url git@github.com:AlanRosenthal/git-repo-move.git --git-branch move_files_example --execute\n```\n\nNote: We're including `click/formatting.py` & `src/click/formatting.py` and `click/parser.py` & `src/click/parser.py`.\nFiles were moved from `click` to `src/click`.\n`git-blame` knows how to capture files history across moves, but `git-filter-branch` does not.\n\nAs you can see, the [`move_files_example` branch](https://github.com/AlanRosenthal/git-repo-move/tree/move_files_example) has contains two files, `formatting.py` and `parser.py`.\nBoth files contain the history from their original repo.\n",
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
