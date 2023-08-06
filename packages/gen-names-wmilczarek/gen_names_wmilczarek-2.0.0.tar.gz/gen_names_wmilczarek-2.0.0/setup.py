# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='gen_names_wmilczarek',
    version='2.0.0',
    description="Generate random names with length",
    long_description='Generate random names with length long',
    long_description_content_type='text/markdown',
    url="https://github.com/treyhunner/names",
    author='Wojciech Milczarek',
    author_email='wojciechjakubmilczarek@gmail.com',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    install_requires=['names'],
)
