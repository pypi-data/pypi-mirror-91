# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezfuse']

package_data = \
{'': ['*']}

install_requires = \
['colorama']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata']}

entry_points = \
{'console_scripts': ['ezfuse = ezfuse.cli:run']}

setup_kwargs = {
    'name': 'ezfuse',
    'version': '1.0.3',
    'description': 'Quickly mount fuse filesystems in temporary directories',
    'long_description': '\n![Github](https://img.shields.io/github/tag/essembeh/ezfuse.svg)\n![PyPi](https://img.shields.io/pypi/v/ezfuse.svg)\n![Python](https://img.shields.io/pypi/pyversions/ezfuse.svg)\n\n\n\n# EzFuse\n\nEzFuse is a tool handle temporary mountpoints for *Fuse* filesystems.\n\nFeatures:\n- automatically create and remove a directory to mount the filesystem\n- interactive shell dialog to execute actions\n- you can mount, umount the mountpoint \n- you can open a shell in the mounted directory\n- you can open your *file browser* in the mounted directory\n- you can exit the *EzFuse*  and keep the mountpoint mounted\n\n![demo.gif](images/demo.gif)\n\n\n# Install\n\nInstall from [Pypi](https://pypi.org/project/ezfuse/)\n```sh\n$ pip3 install --user -U ezfuse\n```\n\nOr install latest version using pip and poetry\n```sh\n$ pip3 install --user -U poetry\n$ pip3 install --user git+https://github.com/essembeh/ezfuse\n```\n\nOr setup a development environment\n```sh\n$ pip3 install --user -U poetry\n$ git clone https://github.com/essembeh/ezfuse\n$ cd ezfuse\n$ poetry install\n$ poetry shell\n(.venv) $ ezfuse --version\n```\n\n\n# Usage\n\nTo mount a remote folder using `sshfs` ensure that `sshfs` is installed on your system before.\n\nWhile the temporary directory is created, *EzFuse* is interactive and you are prompted for an action:\n```sh\n$ ezfuse --type sshfs MYREMOTEHOST:/some/path/here\n[info] Using mountpoint ezmount-sshfs-9dy6yb34\n[exec] sshfs MYREMOTEHOST:/some/path/here ezmount-sshfs-9dy6yb34\n\nx: exit\nq: umount and exit\no: xdg-open\ns: shell\nm: mount\nu: umount\n[x/q/o/s/m/u] \n\n```\n![dialog.png](images/dialog.png)\n\n\nWhen exiting *EzFuse* using `q`, the filesystem will automatically be unmounted and the temporary directory removed.\n\n> Note: All executed commands are displayed with `[exec]` prefix.\n\n\n# Advanced usage: use symlinks\n\nBy default, you have to pass the `-t, --type` to *EzFuse* to specify which *Fuse* filesystem to use, but you can also create symplinks to avoid that.\n\nFor example, to use `sshfs`, create a symlink named `ezsshfs` pointing to `ezfuse` \n\n```sh\n$ mkdir -p ~/.local/bin/\n$ ln -s $(which ezfuse) ~/.local/bin/ezsshfs\n# Now the two commands are equivalent\n$ ezsshfs MYREMOTEHOST:/some/path/here\n$ ezfuse -t sshfs MYREMOTEHOST:/some/path/here\n```\n\nYou can do it for every *Fuse* filesystem you may use, like `borgfs`for example:\n\n```sh\n$ ln -s $(which ezfuse) ~/.local/bin/ezborgfs\n$ ezborgfs /path/to/my/backup.borg/\n```\n\n',
    'author': 'Sébastien MB',
    'author_email': 'seb@essembeh.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/essembeh/ezfuse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
