#!/usr/bin/env python
#
# setup.py for DroidSync
#

import os
import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

import sys
sys.path.insert(0, './src')
from droidsync import version_string


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "DroidSync",
    version = version_string,
    description = "Synchronizes iTunes playlists with a folder (on your Android phone)",
    long_description=read('README.md'),
    author = "Brendan Almonte",
    author_email = "almonteb@datawh.net",
    maintainer = "Dirk Ruediger",
    maintainer_email = "dirk@niebegeg.net",
    url = "https://github.com/almonteb/DroidSync",
    install_requires=[
        'appscript>=1.0.0',
    ],
    entry_points={
        'console_scripts': [
            'droidsync = droidsync:run_main',
        ],
    },
    packages=find_packages('src'),
    package_dir={"": "src"},
    py_modules=[splitext(basename(i))[0] for i in glob.glob("src/*.py")],
    include_package_data=True,
    platforms='OSX',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: End Users/Desktop',
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Multimedia',
    ],
)
