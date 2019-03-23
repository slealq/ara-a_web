# -*- coding: utf-8 -*-

# Learn more: https://github.com/slealq/oddcrawler

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='oddcrawler',
    version='0.1.0',
    description='Simple web crawler to fetch text from news\' webpages. ',
    long_description=readme,
    author='Stuart Leal | Josue Rojas | Sergio Lizano',
    author_email='stuart.leal23@gmail.com',
    url='https://github.com/slealq/oddcrawler',
    license=license,
    packages=find_packages('oddcrawler'),
    install_requires=[]
)
