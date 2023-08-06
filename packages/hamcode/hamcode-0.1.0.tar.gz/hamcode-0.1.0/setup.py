# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hamcode']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'hamcode',
    'version': '0.1.0',
    'description': 'True implementation of Hamming Code on Python',
    'long_description': '',
    'author': 'peach lasagna',
    'author_email': 'kir.kud@inbox.ru',
    'maintainer': 'baskiton',
    'maintainer_email': None,
    'url': 'https://github.com/peach-lasagna/True-Hamming-Code',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
