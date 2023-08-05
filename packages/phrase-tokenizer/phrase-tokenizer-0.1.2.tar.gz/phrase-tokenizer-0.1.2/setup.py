# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['phrase_tokenizer']

package_data = \
{'': ['*']}

install_requires = \
['benepar>=0.1.2,<0.2.0', 'logzero>=1.6.3,<2.0.0', 'tensorflow>=2.4.0,<3.0.0']

setup_kwargs = {
    'name': 'phrase-tokenizer',
    'version': '0.1.2',
    'description': 'Tokenize an English sentence to phrases',
    'long_description': '# Phrase Tokenizer\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/phrase-tokenizer.svg)](https://badge.fury.io/py/phrase-tokenizer)\n\nTokenize an English sentence to phrases\n\n## Installation\n\n```bash\npip install phrase-tokenizer\n# pip install phrase-tokenizer -U to update\n```\n\nOr clone the repo `https://github.com/ffreemt/phrase-tokenizer.git`:\n\n```bash\ngit clone https://github.com/ffreemt/phrase-tokenizer.git\ncd phrase-tokenizer\npip install logzero benepar tensorflow\n```\nOr use `poetry`, e.g.\n```bash\ngit clone https://github.com/ffreemt/phrase-tokenizer.git\ncd phrase-tokenizer\npoetry install\n```\n\n## Usage\n\n```python\nfrom phrase_tokenizer import phrase_tok\n\nres = phrase_tok("Short cuts make long delay.")\nprint(res)\n# [\'Short cuts\', \'make long delay\']\n\n# verbose=True turns on verbose to see the tokenizing process\nres = phrase_tok("Short cuts make long delay", verbose=True)\n# \',..Short.cuts,.make..long.delay..\'\n```\n\nConsult the source code for details.\n\n## For Developers\n\n```bash\ngit clone https://github.com/ffreemt/phrase-tokenizer.git\ncd phrase-tokenizer\npip install -r requirements-dev.txt\n```\n\nIn `jupyter notebook`, ``plot_tree`` is able to draw a nice tree to aid the development, e.g.,\n\n```python\nfrom phrase_tokenizer.phrase_tok import plot_tree\n\nplot_tree("Short cuts make long delay.")\n```\n\n![img](https://github.com/ffreemt/phrase-tokenizer/blob/master/img/short_cuts.png?raw=true)\n\n\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/phrase-tokenizer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
