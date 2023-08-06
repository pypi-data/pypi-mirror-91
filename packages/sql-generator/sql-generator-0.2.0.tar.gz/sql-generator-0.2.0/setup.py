# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sql_generator']

package_data = \
{'': ['*'], 'sql_generator': ['resources/*']}

install_requires = \
['psycopg2>=2.8.6,<3.0.0']

setup_kwargs = {
    'name': 'sql-generator',
    'version': '0.2.0',
    'description': 'A sql generator',
    'long_description': None,
    'author': 'Nils T.',
    'author_email': 'nilsntth@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
