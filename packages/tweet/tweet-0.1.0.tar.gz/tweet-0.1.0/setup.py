# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweet']

package_data = \
{'': ['*']}

install_requires = \
['black>=20.8b1,<21.0',
 'flake8>=3.8.4,<4.0.0',
 'mypy>=0.790,<0.791',
 'python-dotenv>=0.15.0,<0.16.0',
 'python-twitter>=3.5,<4.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tweet = tweet.main:app']}

setup_kwargs = {
    'name': 'tweet',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Portal Gun\n\nThe awesome Portal Gun',
    'author': 'ganariya',
    'author_email': 'ganariya2525@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
