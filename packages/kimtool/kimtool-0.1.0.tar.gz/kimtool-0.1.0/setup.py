#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@File           ：setup.py
@Author         ：Kim
@Date           ：2021/1/13 9:27
@Desc           ：
@Mail           : 913031410@qq.com
@PythonVersion  ：Python3.8.5
'''
from setuptools import setup, find_packages

setup(
    name = "kimtool",
    version = "0.1.0",
    keywords = ("pip", "rpa","kimtool","kim"),
    description = "rpa activity tool",
    long_description = "rpa activity tool",
    license = "MIT Licence",

    url = "https://www.rpa.kingdee.com",
    author = "kim",
    author_email = "913031410@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)