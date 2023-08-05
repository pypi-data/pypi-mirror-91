from setuptools import find_packages, setup, find_namespace_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='casinogv', 
packages=find_namespace_packages(include=['casinogv.*']), 
version='0.0.0.2',
description="Gibson's casino library",
author='Sagiv',
include_package_data=True,
license="MIT", 
long_description=long_description,
long_description_content_type='text/markdown',
setup_requires=['pytest-runner'])
