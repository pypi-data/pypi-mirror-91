#!/usr/bin/env python

from setuptools import setup, find_packages

install_requires = []
tests_require = ["coverage", "flake8", "pexpect", "wheel"]

setup(
    name='taxon',
    version='0.0.1',
    url='https://github.com/kislyuk/taxon',
    project_urls={
        "Documentation": "https://kislyuk.github.io/taxon",
        "Source Code": "https://github.com/kislyuk/taxon",
        "Issue Tracker": "https://github.com/kislyuk/taxon/issues"
    },
    license='Apache Software License',
    author='Andrey Kislyuk',
    author_email='kislyuk@gmail.com',
    description='Taxon',
    long_description=open('README.rst').read(),
    install_requires=install_requires,
    tests_require=tests_require,
    packages=find_packages(exclude=['test'])
)
