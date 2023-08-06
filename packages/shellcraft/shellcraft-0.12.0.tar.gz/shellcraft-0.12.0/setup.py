# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shellcraft']

package_data = \
{'': ['*'], 'shellcraft': ['data/*']}

install_requires = \
['click>=7.0,<8.0', 'protobuf>=3.8,<4.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['shellcraft = shellcraft.cli:main']}

setup_kwargs = {
    'name': 'shellcraft',
    'version': '0.12.0',
    'description': 'ShellCraft is a command line based crafting game.',
    'long_description': "![Cover Image](https://raw.githubusercontent.com/maebert/shellcraft/HEAD/docs/img/cover.png)\n\nShellCraft is a game about mining, crafting, and puzzling, loosely based on Ted Chiang's short story *[Seventy-Two Letters](https://maebert.github.io/shellcraft/72letters)*.\n\n```sh\n# Install ShellCraft (requires python 3)\n$ pip3 install shellcraft\n\n# Run ShellCraft:\n$ shellcraft\n```\n\nRead the [full documentation here](https://maebert.github.io/shellcraft).\n\n![PYPI](https://img.shields.io/pypi/v/shellcraft.svg)\n![Travis](https://img.shields.io/travis/maebert/shellcraft.svg)\n![PyUp](https://pyup.io/repos/github/maebert/shellcraft/shield.svg)\n![Black](https://img.shields.io/badge/code%20style-black-000000.svg)\n",
    'author': 'Manuel Ebert',
    'author_email': 'manuel@1450.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://maebert.github.io/shellcraft',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
