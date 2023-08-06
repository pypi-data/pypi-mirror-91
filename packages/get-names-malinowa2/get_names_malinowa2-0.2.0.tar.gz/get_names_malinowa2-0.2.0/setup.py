# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='get_names_malinowa2',
    version='0.2.0',
    author='malinowa',
    author_email='amt-mal@wp.pl',
    packages=find_packages(),
    include_package_data=True,
    description='Package with functions printing random names, surnames, or both',
    long_description='Package with functions printing random names, surnames, or both',
    long_description_content_type='text/markdown',
    keyword='get-names',
    install_requires=['names']
)
