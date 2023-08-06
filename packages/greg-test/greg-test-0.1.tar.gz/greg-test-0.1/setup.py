# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['greg_test']

package_data = \
{'': ['*']}

install_requires = \
['click', 'pudb', 'pytest', 'pytest-sugar']

entry_points = \
{'console_scripts': ['greg-test = greg_test.cli:main']}

setup_kwargs = {
    'name': 'greg-test',
    'version': '0.1',
    'description': '',
    'long_description': '# greg-test\n\n> A cool project\n\n**v0.1**\n\n-----\n\n## In action\n\nText\n',
    'author': 'Greg Henry',
    'author_email': 'mail.greg.henry@gmail.com',
    'maintainer': 'Greg Henry',
    'maintainer_email': 'mail.greg.henry@gmail.com',
    'url': 'https://github.com/GregoireHENRY/greg-test',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
