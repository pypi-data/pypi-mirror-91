# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['igenius_adapters_sdk', 'igenius_adapters_sdk.entities']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'igenius-adapters-sdk',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'iGenius Backend',
    'author_email': 'backend@igenius.ai',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
