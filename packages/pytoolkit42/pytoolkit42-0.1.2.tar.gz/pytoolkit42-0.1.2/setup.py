# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytoolkit']

package_data = \
{'': ['*']}

install_requires = \
['fastcore>=1.3.18,<2.0.0', 'typeguard>=2.10.0,<3.0.0']

setup_kwargs = {
    'name': 'pytoolkit42',
    'version': '0.1.2',
    'description': 'Collection of useful utilities and tools for python projects',
    'long_description': '# pytoolkit\n\n[![Python](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8-green.svg)](https://www.python.org/)\n[![PyPI version](https://badge.fury.io/py/pytoolkit42.svg)](https://badge.fury.io/py/pytoolkit42)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Docs](https://readthedocs.org/projects/pytoolkit42/badge/?version=latest)](https://pytoolkit42.readthedocs.io/en/latest)\n[![GitHub Activity](https://img.shields.io/github/commit-activity/y/HazardDede/pytoolkit.svg)](https://github.com/HazardDede/pytoolkit/commits/main)\n[![Build Status](https://travis-ci.org/HazardDede/pytoolkit.svg?branch=main)](https://travis-ci.org/HazardDede/pytoolkit)\n[![Coverage Status](https://coveralls.io/repos/github/HazardDede/pytoolkit/badge.svg?branch=main)](https://coveralls.io/github/HazardDede/pytoolkit?branch=main)\n![Project Maintenance](https://img.shields.io/badge/maintainer-Dennis%20Muth%20%40HazardDede-blue.svg)\n\n\n> Collection of useful utilities and tools for python projects\n\n## Installation\n\n```bash\npip install pytoolkit42\n```\n\n## Purpose\n\nPretty much every utility stuff you could imagine is already written down in some python package.\nBut almost every time these stuff is part of a heavyweight framework with a lots of\ndependencies. And on top they do it in a slightly different way - you would do it - because it\nis tailored to their needs.\n\nThis is why I made up this `Yet Another Utility Package` called `pytoolkit42`.\nI want this `toolkit` to be\n\n* lightweight and\n* easy to use\n\nRight now it does not have the answer to every problem you will encounter, but it serves\nwell to solve problems I stumble upon on a regular basis.\n\nThe collection of functions, classes, decorator, mixins will grow when I come up with a\nsolution that seems to be of use for everybody else out there.\n\nBut to be honest: I try to make this package as generic as possible so it might be useful to you,\nbut I cannot promise. Nevertheless you are encouraged to make PRs.\n\n## Manual\n\nThe manual is available at Read the Docs:\n\n  [https://pytoolkit42.readthedocs.io/en/latest/](https://pytoolkit42.readthedocs.io/en/latest/)',
    'author': 'Dennis Muth',
    'author_email': 'd.muth@gmx.net',
    'maintainer': 'Dennis Muth',
    'maintainer_email': 'd.muth@gmx.net',
    'url': 'https://github.com/HazardDede/pytoolkit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
