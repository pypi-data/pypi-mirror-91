# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['astro_ph']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=3.141,<4.0', 'typing-extensions>=3.7,<4.0']

setup_kwargs = {
    'name': 'astro-ph',
    'version': '0.1.0',
    'description': 'Post astro-ph articles translated by DeepL to Slack',
    'long_description': '# astro-ph\n\n[![PyPI](https://img.shields.io/pypi/v/astro-ph.svg?label=PyPI&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Python](https://img.shields.io/pypi/pyversions/astro-ph.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/project/astro-ph/)\n[![Test](https://img.shields.io/github/workflow/status/astropenguin/astro-ph/Test?logo=github&label=Test&style=flat-square)](https://github.com/astropenguin/astro-ph/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nPost astro-ph articles translated by DeepL to Slack\n',
    'author': 'Akio Taniguchi',
    'author_email': 'taniguchi@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/astropenguin/astro-ph/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
