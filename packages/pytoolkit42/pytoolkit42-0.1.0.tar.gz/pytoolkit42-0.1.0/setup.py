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
    'version': '0.1.0',
    'description': 'Collection of useful utilities and tools for python projects',
    'long_description': '# pytoolkit\n\n[![Python](https://img.shields.io/badge/Python-3.6%20%7C%203.7%20%7C%203.8-green.svg)](https://www.python.org/)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Docs](https://readthedocs.org/projects/pytoolkit42/badge/?version=latest)](https://pytoolkit42.readthedocs.io/en/latest)\n[![GitHub Activity](https://img.shields.io/github/commit-activity/y/HazardDede/pytoolkit.svg)](https://github.com/HazardDede/pytoolkit/commits/main)\n[![Build Status](https://travis-ci.org/HazardDede/pytoolkit.svg?branch=main)](https://travis-ci.org/HazardDede/pytoolkit)\n[![Coverage Status](https://coveralls.io/repos/github/HazardDede/pytoolkit/badge.svg?branch=main)](https://coveralls.io/github/HazardDede/pytoolkit?branch=main)\n![Project Maintenance](https://img.shields.io/badge/maintainer-Dennis%20Muth%20%40HazardDede-blue.svg)\n\n\n> Collection of useful utilities and tools for python projects\n\n## Installation\n\n```bash\npip install pytoolkit\n```\n\n## Tools\n\nTBD',
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
