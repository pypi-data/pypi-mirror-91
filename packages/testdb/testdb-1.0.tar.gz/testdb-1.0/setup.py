#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

setup(
    name="testdb",
    version="1.0",
    keywords=("test", "xxx"),
    description="db sdk",
    long_description="db sdk for python",
    license="MIT Licence",

    url="http://test.com",
    author="chaizc",
    author_email="chaizc@gmail.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['psycopg2>=2.8.6','sqlalchemy==1.3.22'],

    scripts=[],
    # entry_points={
    #     'console_scripts': [
    #         'test = test.help:main'
    #     ]
    # }
)
