# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tweet']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=0.15.0,<0.16.0',
 'python-twitter>=3.5,<4.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['tweet = tweet.main:app']}

setup_kwargs = {
    'name': 'tweet',
    'version': '1.0.1',
    'description': '',
    'long_description': 'tweet\n\n---\n\n`tweet` can tweet now your status from CLI easily.  \n`tweet` cat tweet `only`, so you will not be distracted.\n\n## How to Install\n\n```\npip install tweet\n```\n\n## How to Use\n\n```\ntweet {your-message}\n```\n\n## How to set up\n\nYou have to set up `~/.twitter-env` file to your home directory yourself.\n\n`~/.twitter-env`\n\n```env\nCONSUMER_TOKEN=.......\nCONSUMER_SECRET=.......\nACCESS_TOKEN=.......\nACCESS_SECRET=.....\n```\n',
    'author': 'ganariya',
    'author_email': 'ganariya2525@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Ganariya/tweet',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
