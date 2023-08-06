# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_mkdocs_shenxzh']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'poetry-mkdocs-shenxzh',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'shenxiangzhuang',
    'author_email': '1021550072@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
