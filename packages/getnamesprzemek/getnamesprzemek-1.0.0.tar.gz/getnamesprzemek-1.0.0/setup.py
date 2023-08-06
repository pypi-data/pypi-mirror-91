# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='getnamesprzemek',
    version='1.0.0',
    description="Generate random names with lenght",
    long_description='Generate random names with lenght long',
    long_description_content_type='text/markdown',
    url="https://github.com/treyhunner/names",
    author='Przemek Dmowski',
    author_email='przemek_dei@op.pl',
    include_package_data=True,
    keywords='random names',
    packages=find_packages(),
    install_requires=['names']
)