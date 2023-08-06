#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import find_packages,setup

setup(
    name='gen_names_bsklodow',
    version='1.0.1',
    description="Generate random names with lenght",
    long_description='Generate random names with lenght long',
    long_description_content_type='text/markdown',
    url="https://github.com/treyhunner/names",
    author='Bartosz Skłodowski',
    author_email='sklodowski94@gmail.com',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    install_requires=['names'],
    scripts = ['getnamesbsklodow/getnames.py', 'bin/getnames.bat']
)
