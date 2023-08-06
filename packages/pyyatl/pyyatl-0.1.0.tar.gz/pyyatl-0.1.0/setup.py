# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yatl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyyatl',
    'version': '0.1.0',
    'description': 'YAML Templating Language',
    'long_description': '',
    'author': 'Dan Hipschman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d5h-foss/yatl',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
