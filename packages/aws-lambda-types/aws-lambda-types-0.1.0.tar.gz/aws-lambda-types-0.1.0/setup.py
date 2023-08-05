# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_lambda_types']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'aws-lambda-types',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Eduard Iskandarov',
    'author_email': 'eduard.iskandarov@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
