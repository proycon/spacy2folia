#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import io
from setuptools import setup


def read(fname):
    return io.open(os.path.join(os.path.dirname(__file__), fname),'r',encoding='utf-8').read()

setup(
    name = "Spacy2FoLiA",
    version = "0.3.2", #also change in __init__.py
    author = "Maarten van Gompel",
    author_email = "proycon@anaproy.nl",
    description = ("Library that adds FoLiA (format for linguistic annotation) support to spaCy"),
    license = "GPL",
    keywords = "nlp computational_linguistics spacy linguistics toolkit folia",
    url = "https://proycon.github.io/folia",
    packages=['spacy2folia'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points = {
        'console_scripts': [
            'spacy2folia = spacy2folia.spacy2folia:main',
        ]
    },
    #include_package_data=True,
    install_requires=['folia >= 2.0.4', 'spacy >= 2.1']
)
