# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['splitem']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['splitem = splitem.cli:run']}

setup_kwargs = {
    'name': 'splitem',
    'version': '0.1.0',
    'description': 'Tool for splitting Kubernetes Manifests into individual files',
    'long_description': '',
    'author': 'Buck Brady',
    'author_email': 'buck@voidrot.dev',
    'maintainer': 'Buck Brady',
    'maintainer_email': 'buck@voidrot.dev',
    'url': 'https://github.com/voidrot/splitem',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
