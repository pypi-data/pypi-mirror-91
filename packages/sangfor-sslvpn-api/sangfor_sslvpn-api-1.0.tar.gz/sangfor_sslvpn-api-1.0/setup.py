#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages
setup(name='sangfor_sslvpn-api',
      version=1.0,
    description=(
        'sangfor_sslvpn_api'
    ),
    long_description=open('README.rst').read(),
    author='Kac001',
    author_email='jleung@qq.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/Kac001/sangfor_sslvpn_api',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries'
    ],
)