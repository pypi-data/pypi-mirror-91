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
    'version': '1.0.1',
    'description': 'The iGenius Software Development Kit to develop crystal datasource adapters.',
    'long_description': '# iGenius Adapters SDK\n\nThis is the Software Development Kit for iGenius Web Connectors development.  \nYou can use our SDK in your project to be able to handle correctly the data structures that will be used by iGenius services to call your web connector adapter.\n\n## Introduction\n\n### Folder structure\n\nOur SDK has the main objective to expose our data structures that are the business objects of our application: we call them `Entities` and thet are included in a package with the same name.\n\n```bash\n-- src\n   |- igenius_adapters_sdk\n      |- entities\n```\n\n### Data structure\n\nOur datasource adapters system is based on a relational database structure, so our `entities` are a mapping of this kind of data organisation.\n\n## Install\n\nWith Poetry\n\n```bash\npoetry add igenius-adapters-sdk\n```\n\nWith pip\n\n```bash\npip install igenius-adapters-sdk\n```\n',
    'author': 'iGenius Backend',
    'author_email': 'backend@igenius.ai',
    'url': 'https://igenius.ai',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
