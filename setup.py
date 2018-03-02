#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A Flask extension that prevents browser access to API. """

import os
import sys
import flask_fool

from setuptools import find_packages, setup
from setuptools.command.install import install


def readme():
    """ Transform the given markdown README to RST. """
    try:
        from m2r import parse_from_file
        return parse_from_file('README.md')
    except ImportError:
        with open('README.md') as stream:
            return stream.read()


class VerifyVersionCommand(install):
    """ Custom command to verify that the git tag matches our version """

    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')
        if tag != flask_fool.__version__:
            sys.exit(
                'Git tag %s does not match the current flask fool version %s'
                % (tag, flask_fool.__version__))

_URL = 'https://github.com/Faylixe/flask-fool'
_TAG_URL = _URL + '/archive/%s.tar.gz'

setup(
    name='flask-fool',
    version=flask_fool.__version__,
    description=__doc__,
    long_description=readme(),
    keywords='flask fool',
    license='Apache Licence 2.0',
    author='Felix Voituret',
    author_email='felix@voituret.fr',
    url=_URL,
    download_url=_TAG_URL % flask_fool.__version__,
    packages=['flask_fool'],
    include_package_data=True,
    install_requires=['flask'],
    cmdclass={'verify': VerifyVersionCommand},
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
    ]
)
