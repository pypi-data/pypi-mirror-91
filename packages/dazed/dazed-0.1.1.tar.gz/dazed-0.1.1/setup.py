# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dazed']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.5,<2.0.0']

extras_require = \
{'pandas': ['pandas>=1.1.5,<2.0.0']}

setup_kwargs = {
    'name': 'dazed',
    'version': '0.1.1',
    'description': 'A confusion matrix package.',
    'long_description': None,
    'author': 'calmdown13',
    'author_email': 'callum@callumdownie.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
