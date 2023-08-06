# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuibit']

package_data = \
{'': ['*'], 'kuibit': ['data/*']}

install_requires = \
['h5py>=2.10.0,<3.0.0', 'numpy>=1.18.5,<2.0.0', 'scipy>=1.5.2,<2.0.0']

extras_require = \
{'full': ['numba>=0.51.2,<0.52.0',
          'lalsuite>=6.77,<7.0',
          'pycbc>=1.16.10,<2.0.0']}

setup_kwargs = {
    'name': 'kuibit',
    'version': '1.0.0b0',
    'description': 'Read and analyze Einstein Toolkit simulations.',
    'long_description': '<p align="center">\n<img src="https://github.com/Sbozzolo/kuibit/raw/master/logo.png" height="150">\n</p>\n\n[![codecov](https://codecov.io/gh/Sbozzolo/kuibit/branch/master/graph/badge.svg)](https://codecov.io/gh/Sbozzolo/kuibit)\n![Tests and documentation](https://github.com/Sbozzolo/kuibit/workflows/Tests/badge.svg)\n[![GPLv3\nlicense](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)\n[![Get help on Telegram](https://img.shields.io/badge/Get%20help%20on-Telegram-blue.svg)](https://t.me/kuibit)\n[![DeepSource](https://static.deepsource.io/deepsource-badge-light-mini.svg)](https://deepsource.io/gh/Sbozzolo/kuibit/?ref=repository-badge)\n\n# kuibit\n\n`kuibit` is a Python library to analyze simulations performed with the Einstein\nToolkit largely inspired by\n[PostCactus](https://github.com/wokast/PyCactus/tree/master/PostCactus).\n`kuibit` can read simulation data and represent it with high-level classes. For\na list of features available, look at the [official\ndocumentation](https://sbozzolo.github.io/kuibit).\n\n## Installation\n\n``kuibit`` is available in PyPI. To install it with `pip`\n``` bash\npip3 install kuibit\n```\nIf they are not already available, `pip` will install all the necessary dependencies.\n\nThe minimum version of Python required is 3.6.\n\nIf you intend to develop ``kuibit``, follow the instruction below.\n\n### Development\n\nFor development, we use [poetry](https://python-poetry.org/). Poetry simplifies\ndependency management, building, and publishing the package.\n\nTo install `kuibit` with poetry, clone this repo, move into the folder, and run:\n``` sh\npoetry install -E full\n```\nThis will download all the needed dependencies in a sandboxed environment (the\n`-E full` flag is for the optional dependencies). When you want to use\n``kuibit``, just run ``poetry shell``. This will drop you in a shell in\nwhich you have full access to ``kuibit`` in "development" version, and its\ndependencies (also the one needed only for development).\n\n## Documentation\n\n`kuibit` uses Sphinx to generate the documentation. To produce the documentation\n```sh\ncd docs && make html\n```\nDocumentation is automatically generated after each commit by GitHub Actions.\n\nWe use [nbsphinx](https://nbsphinx.readthedocs.io/) to translate Jupyter\nnotebooks to the examples. The extension is required. Note: Jupyter notebooks\nhave to be un-evaluated. `nbsphinx` requires [pandoc](https://pandoc.org/). If\ndon\'t have `pandoc`, you should comment out `nbsphinx` in `docs/conf.py`, or\ncompiling the documentation will fail.\n\n## Tests\n\n`kuibit` comes with a suite of unit tests. To run the tests, (in a poetry shell),\n```sh\npoetry run python -m unittest\n```\nTests are automatically run after each commit by GitHub Actions.\n\nIf you want to look at the coverage of your tests, run (in a poetry shell)\n```sh\ncoverage run -m unittest\ncoverage html\n```\nThis will produce a directory with the html files containing the analysis of\nthe coverage of the tests.\n\n## Experimental branch\n\nThe git repo of `kuibit` has an `experimental` branch, which contains\nmodules for visualization and several general-purpose scripts (e.g., to plot a\ngiven grid variable via command-line). It is worth to have a look at that branch\ntoo.\n\n## What is a _kuibit_?\n\nA kuibit (harvest pole) is the tool traditionally used by the Tohono O\'odham\npeople to reach the fruit of the Saguaro cacti during the harvesting season. In\nthe same way, this package is a tool that you can use to collect the fruit of\nyour `Cactus` simulations.\n\n## Credits\n\n`kuibit` follows the same designed as `PostCactus`, code developed by Wolfgang\nKastaun. This fork completely rewrites the original code, adding emphasis on\ndocumentation, testing, and extensibility. The logo contains elements designed\nby [freepik.com](freepik.com).\n\n',
    'author': 'Gabriele Bozzola',
    'author_email': 'gabrielebozzola@arizona.edu',
    'maintainer': 'Gabriele Bozzola',
    'maintainer_email': 'gabrielebozzola@arizona.edu',
    'url': 'https://github.com/sbozzolo/kuibit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
