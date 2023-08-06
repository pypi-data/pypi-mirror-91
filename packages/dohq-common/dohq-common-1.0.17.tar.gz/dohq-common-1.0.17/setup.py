#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
import os

__version__ = '1.0'

devStatus = '4 - Beta'  # https://pypi.python.org/pypi?%3Aaction=list_classifiers

if 'TRAVIS_BUILD_NUMBER' in os.environ and 'TRAVIS_BRANCH' in os.environ:
    print("This is TRAVIS-CI build")
    print("TRAVIS_BUILD_NUMBER = {}".format(os.environ['TRAVIS_BUILD_NUMBER']))
    print("TRAVIS_BRANCH = {}".format(os.environ['TRAVIS_BRANCH']))

    __version__ += '.{}{}'.format(
        '' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ['TRAVIS_BRANCH'] == 'master' else 'dev',
        os.environ['TRAVIS_BUILD_NUMBER'],
    )

    devStatus = '5 - Production/Stable' if 'release' in os.environ['TRAVIS_BRANCH'] or os.environ[
        'TRAVIS_BRANCH'] == 'master' else devStatus

else:
    print("This is local build")
    __version__ += '.dev0'

print("dohq-common build version = {}".format(__version__))

setup(
    name='dohq-common',

    version=__version__,

    description='Common libs for devopshq tools',

    long_description='Common libs for devopshq tools',

    license='MIT',

    author='Open DevOps Community',

    author_email='devopshq@gmail.com',

    url='https://devopshq.github.io/common/',

    download_url='https://github.com/devopshq/common.git',

    classifiers=[
        'Development Status :: {}'.format(devStatus),
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python :: 3.7',
    ],

    keywords=[
        'DevOpsHQ',
        'devops',
    ],

    packages=[
        'dohq_common',
    ],

    setup_requires=[
    ],

    tests_require=[
        'pytest',
    ],

    install_requires=[
    ],

    package_data={
        "": [
            "./dohq_common/*.py",

            "./tests/*.py",

            "LICENSE",
            "README.md",
            "README_RU.md",
        ],
    },

    zip_safe=True,
)
