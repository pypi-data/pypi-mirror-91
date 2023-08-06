#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: zhangkai
Email: kai.zhang1@nio.com
Last modified: 2019-04-07 00:07:43
'''

from setuptools import setup

setup(
    name="kkutils",
    version="1.3.7",
    description="digua python utils",
    author="zhangkai",
    author_email="zkdfbb@qq.com",
    url="https://ishield.cn",
    license="MIT",
    python_requires='>=3.5',
    data_files=[('', ['requirements.txt'])],
    install_requires=[line.strip() for line in open('requirements.txt') if not line.strip().startswith('#')],
    include_package_data=True,
    py_modules=[
        'spider',
    ],
    packages=[
        'tornado_utils',
        'utils',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
