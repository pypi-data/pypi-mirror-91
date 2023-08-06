#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: platformhandler.py
# @time: 2019/4/30 13:30
# @Software: PyCharm

from setuptools import setup, find_packages
from snowland_py253 import version
from astartool.setuptool import get_version, load_install_requires

setup(
    name="snowland-py253",
    version=get_version(version),
    description=(
        'Python3 SDK for 253.com (SMS)'
    ),
    long_description=open('README.rst', encoding='utf-8').read(),
    author='A.Star',
    author_email='astar@snowland.ltd',
    maintainer='A.Star',
    maintainer_email='astar@snowland.ltd',
    license='Apache v2.0 License',
    packages=find_packages(),
    platforms=["all"],
    url='https://gitee.com/snowlandltd/snowland-253-python',
    classifiers=[
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=load_install_requires(),
)
