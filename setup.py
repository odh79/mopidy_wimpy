from __future__ import unicode_literals

import re

from setuptools import find_packages, setup


def get_version(filename):
    with open(filename) as fh:
        metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", fh.read()))
        return metadata['version']


setup(
    name='Mopidy-Wimpy',
    version=get_version('mopidy_wimpy/__init__.py'),
    url='https://github.com/daniel@hansson.homeip.net/mopidy-wimpy',
    license='Apache License, Version 2.0',
    author='Daniel Hansson',
    author_email='daniel@hansson.homeip.net',
    description='Mopidy extension for Wimp',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.19',
        'Pykka >= 1.1',
    ],
    entry_points={
        'mopidy.ext': [
            'wimpy = mopidy_wimpy:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
