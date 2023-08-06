#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:58:27 2019

@author: timepi

@description: this is a python lib
"""
from setuptools import setup, find_packages

setup(
    name='ulibpy',
    version='0.0.1',
    keywords=('pip', 'prome'),
    description='common use lib',
    long_description='common use lib',
    license='GNU General Public License v3.0',
    url='https://github.com/uopensail/ulibpy.git',
    author='timepi',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['toml >= 0.10.2', 'prometheus_client >= 0.7.1']
)
