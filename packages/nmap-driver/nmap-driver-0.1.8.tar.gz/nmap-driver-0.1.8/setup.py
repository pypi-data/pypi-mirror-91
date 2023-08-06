#!/usr/bin/env python
# -*- coding:utf-8 -*-


from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import call

class CustomInstall(install):
    def run(self):
        install.run(self)
        call(['pip', 'install', '--no-binary=protobuf', 'protobuf'])

setup(
    name = 'nmap-driver',
    version = '0.1.8',
    keywords='wx',
    description = 'a library for nmap scan',
    license = 'MIT License',
    url = 'https://192.168.1.146:8081/repo/packages',
    author = 'superman',
    author_email = '646390966@qq.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
'exception==0.1.0',
'grpcio==1.32.0',
'ipdb==0.13.4',
'pid==3.0.4',
'python-daemon==2.2.4',
'python-nmap==0.6.1',
'configparser==5.0.1',
'PyJWT==1.7.1'
],
cmdclass={
          'install': CustomInstall, }
)

