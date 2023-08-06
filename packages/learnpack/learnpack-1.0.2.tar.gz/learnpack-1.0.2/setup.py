# -*- coding: utf-8 -*-
# @Time    : 2021/1/13 4:42 下午
# @Author  : haohao
# @FileName: setup.py

import setuptools
with open("README.md","r") as f:
    long_description=f.read()

setuptools.setup(
    name='learnpack',
    version='1.0.2',
    author='haohao',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['test_case1'],
)