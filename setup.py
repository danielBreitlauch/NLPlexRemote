#!/usr/bin/python
"""
Install NLPlexRemote
"""
from distutils.core import setup
from setuptools import find_packages

setup(
    name='NLPlexRemote',
    version='0.1.0',
    description='Remote control Plex clients with natural language.',
    author='Daniel Breitlauch',
    author_email='github@flying-stampe.de',
    url='https://github.com/danielBreitlauch/NLPlexRemote',
    license='MIT',
    packages=find_packages(),
    dependency_links=['https://github.com/danielBreitlauch/python-plexapi/zipball/master#egg=PlexAPI'],
    install_requires=[
        'PlexAPI',
        'mock'
    ],
    long_description=open('README.md').read(),
    keywords=['plex', 'natural language', 'nlp', 'remote'],
)
