# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pwninit']
entry_points = \
{'console_scripts': ['pwninit = entry:main']}

setup_kwargs = {
    'name': 'pwninit',
    'version': '0.1.0',
    'description': 'pwnable challenge quick starter.',
    'long_description': None,
    'author': 'ICEB3AR',
    'author_email': '!dong992016',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
