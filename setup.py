# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='life_game',
    version='0.1.0',
    description='everyone can play lifegame with Python',
    long_description=readme,
    author='Ken.K',
    author_email='yosyuaomenw at yahoo.co.jp',
    url='https://github.com/seven320/life_game',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'pygame',
        'numpy',
        'time',
        'copy',
    ]
    )
