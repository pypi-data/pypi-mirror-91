# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['cdown']

package_data = \
{'': ['*']}

install_requires = \
['click', 'gitignore_parser']

extras_require = \
{'docs': ['sphinx>=1.3', 'sphinx-rtd-theme']}

entry_points = \
{'console_scripts': ['cdown = cdown.cli:code_owners_cli']}

setup_kwargs = {
    'name': 'cdown',
    'version': '0.1.0',
    'description': 'Tools for CODEOWNERS files',
    'long_description': '========\nOverview\n========\n\n.. start-badges\n\n.. list-table::\n    :stub-columns: 1\n\n    * - docs\n      - |docs|\n    * - tests\n      - |\n        | |codecov|\n    * - package\n      - | |version| |wheel| |supported-versions| |supported-implementations|\n        | |commits-since|\n.. |docs| image:: https://readthedocs.org/projects/python-cdown/badge/?style=flat\n    :target: https://readthedocs.org/projects/python-cdown\n    :alt: Documentation Status\n\n.. |codecov| image:: https://codecov.io/gh/andreoliwa/python-cdown/branch/master/graphs/badge.svg?branch=master\n    :alt: Coverage Status\n    :target: https://codecov.io/github/andreoliwa/python-cdown\n\n.. |version| image:: https://img.shields.io/pypi/v/cdown.svg\n    :alt: PyPI Package latest release\n    :target: https://pypi.org/project/cdown\n\n.. |wheel| image:: https://img.shields.io/pypi/wheel/cdown.svg\n    :alt: PyPI Wheel\n    :target: https://pypi.org/project/cdown\n\n.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/cdown.svg\n    :alt: Supported versions\n    :target: https://pypi.org/project/cdown\n\n.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/cdown.svg\n    :alt: Supported implementations\n    :target: https://pypi.org/project/cdown\n\n.. |commits-since| image:: https://img.shields.io/github/commits-since/andreoliwa/python-cdown/v0.1.0.svg\n    :alt: Commits since latest release\n    :target: https://github.com/andreoliwa/python-cdown/compare/v0.1.0...master\n\n\n\n.. end-badges\n\nTools for code owners files\n\n* Free software: MIT license\n\nInstallation\n============\n\n::\n\n    pip install cdown\n\nYou can also install the in-development version with::\n\n    pip install https://github.com/andreoliwa/python-cdown/archive/master.zip\n\n\nDocumentation\n=============\n\n\nhttps://python-cdown.readthedocs.io/\n\n\nDevelopment\n===========\n\nTo run all the tests run::\n\n    tox\n\nNote, to combine the coverage data from all the tox environments run:\n\n.. list-table::\n    :widths: 10 90\n    :stub-columns: 1\n\n    - - Windows\n      - ::\n\n            set PYTEST_ADDOPTS=--cov-append\n            tox\n\n    - - Other\n      - ::\n\n            PYTEST_ADDOPTS=--cov-append tox\n',
    'author': 'W Augusto Andreoli',
    'author_email': 'andreoliwa@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreoliwa/python-cdown',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
