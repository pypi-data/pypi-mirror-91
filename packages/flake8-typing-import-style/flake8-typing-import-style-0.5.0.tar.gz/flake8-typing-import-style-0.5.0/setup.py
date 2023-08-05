# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_typing_import_style']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3.8.4,<4.0.0', 'setuptools']

entry_points = \
{'flake8.extension': ['I9 = flake8_typing_import_style:I9']}

setup_kwargs = {
    'name': 'flake8-typing-import-style',
    'version': '0.5.0',
    'description': 'A flake8 plugin to ensure typing module import convention',
    'long_description': "# flake8-import-style\n\n[![Build](https://img.shields.io/travis/sfstpala/flake8-import-style.svg?style=flat-square)](https://travis-ci.org/sfstpala/flake8-import-style)\n[![Coverage](https://img.shields.io/coveralls/sfstpala/flake8-import-style.svg?style=flat-square)](https://coveralls.io/r/sfstpala/flake8-import-style)\n[![PyPI](https://img.shields.io/pypi/v/flake8-import-style.svg?style=flat-square)](https://pypi.python.org/pypi/flake8-import-style)\n\nA [flake8](http://flake8.pycqa.org/en/latest/) plugin to ensure explicit module imports.\n\n    pip install flake8_typing_import_style\n    flake8 *.py\n\nErrors (enabled by default):\n\n - `I801 use 'import ...' instead of 'from ... import ...'`\n\nTested with Python 2.7, 3.4, 3.5, and 3.6.\n\nType `make test` or `tox` to run the test suite in a virtual environment.\n",
    'author': 'Stefano Palazzo',
    'author_email': 'stefano.palazzo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jnoortheen/flake8-import-style',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
