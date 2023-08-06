# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['all_relative']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['all-relative = all_relative.main:main']}

setup_kwargs = {
    'name': 'all-relative',
    'version': '0.1.7',
    'description': 'cli tool to convert a static site to use only relative urls',
    'long_description': '# all-relative\n',
    'author': 'Ivan Gonzalez',
    'author_email': 'scratchmex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scratchmex/all-relative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
