#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Guillaume Fournier <fournierg@gmail.com>
#
# This code is distributed under the terms and conditions
# from the MIT License (MIT).
import io
import os

from setuptools import setup, find_packages


def _get_version():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(curr_dir, 'smart_pathlib', 'version.py')) as fin:
        line = fin.readline().strip()
        parts = line.split(' ')
        assert len(parts) == 3
        assert parts[0] == '__version__'
        assert parts[1] == '='
        return parts[2].strip('\'"')


__version__ = _get_version()


def read(fname):
    return io.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


gcp_deps = ['google-cloud-storage']

all_deps = gcp_deps
tests_require = all_deps + [
    'pytest',
]

setup(
    name='smart_pathlib',
    version=__version__,
    description='Utils for making os standard path operations'
                'interoperable with Cloud blob storages',
    long_description=read('README.md'),

    packages=find_packages(exclude=("tests",)),
    package_data={
        "smart_pathlib.tests": ["tests/resources/*"],
    },

    author='Guillaume Fournier',
    author_email='fournierg@gmail.com',
    maintainer='Guillaume Fournier',
    maintainer_email='fournierg@gmail.com',

    url='https://github.com/gfournier/smart_pathlib',
    download_url='http://pypi.python.org/pypi/smart_pathlib',

    keywords='s3, hdfs, gcs, azure blob storage',

    license='MIT',
    platforms='any',

    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'gcp': gcp_deps,
        'all': all_deps,
    },
    python_requires=">=3.6.*",

    test_suite="smart_pathlib.tests",

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: System :: Distributed Computing',
        'Topic :: Database :: Front-Ends',
    ],
)
