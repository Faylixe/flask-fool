#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" TODO : Document. """

import os

from setuptools import find_packages, setup

readme = open('README.md').read()

tests_require = ['pytest>=2.8.0']
setup_requires = ['pytest-runner>=2.6.2']
install_requires = ['Flask>=0.10']

extras_require = { 'tests': tests_require }
extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

packages = find_packages()

setup(
    name='Flask-Fool',
    version='1.0.0',
    description=__doc__,
    long_description=readme,
    keywords='flask fool',
    license='Apache Licence 2.0',
    author='Faylixe',
    author_email='felix@voituret.fr',
    url='https://github.com/Faylixe/flask-fool',
    download_url='https://github.com/Faylixe/flask-fool/archive/1.0.0.tar.gz',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 5 - Production/Stable',
    ],
)