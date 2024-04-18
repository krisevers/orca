# -*- coding: utf-8 -*-

# Learn more: https://github.com/krisevers/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='orca',
    version='0.1.0',
    description='Orca Package',
    long_description=readme,
    author='Kris Evers',
    author_email='krisevers14@gmail.com',
    url='https://github.com/krisevers/orca',
    license=license,
    packages=find_packages(exclude=('tests', 'docs', 'examples'))
)
