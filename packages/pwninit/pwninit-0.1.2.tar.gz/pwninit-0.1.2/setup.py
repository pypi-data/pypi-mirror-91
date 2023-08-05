# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pwninit']
entry_points = \
{'console_scripts': ['pwninit = pwninit:main']}

setup_kwargs = {
    'name': 'pwninit',
    'version': '0.1.2',
    'description': 'pwnable challenge quick starter.',
    'long_description': None,
    'author': 'exd0tpy',
    'author_email': 'jsw5258@ajou.ac.kr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
