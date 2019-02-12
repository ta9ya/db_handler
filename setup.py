# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='db_handler',
    version='0.1.0',
    description='DataBase handler',
    long_description=readme,
    author='tiwa',
    author_email='t.iwasa0821@gmail.com',
    url='https://github.com/ta9ya/db_handler.git',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=['requests', 'configparser', 'json', 'os']
)

