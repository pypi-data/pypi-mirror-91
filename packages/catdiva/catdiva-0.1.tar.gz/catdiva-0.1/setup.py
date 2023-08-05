# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['catdiva']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'catdiva',
    'version': '0.1',
    'description': 'print(catdiva.cat())',
    'long_description': None,
    'author': 'TheMisterSenpai',
    'author_email': '61903983+TheMisterSenpai@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
