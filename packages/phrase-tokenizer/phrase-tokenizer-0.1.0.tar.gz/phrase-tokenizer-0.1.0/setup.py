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
    'version': '0.1.0',
    'description': 'Tokenize an English sentence to phrases',
    'long_description': None,
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
