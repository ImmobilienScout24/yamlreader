#!/usr/bin/env python

from setuptools import setup, find_packages
import sys
sys.path.insert(0, "src")
from yamlreader import __version__
sys.path.pop(0)
from distutils.command.clean import clean
import os
import shutil

class completeClean(clean):
    def run(self):
        if os.path.exists(self.build_base):
            shutil.rmtree(self.build_base)
            
        dist_dir = 'dist'
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)
        dist_dir = "deb_dist"
        if os.path.exists(dist_dir):
            shutil.rmtree(dist_dir)

setup(
    name="yamlreader",
    version=__version__,
    author="Schlomo Schapiro",
    author_email='schlomo.schapiro@immobilienscout24.de',
    description="Merge YAML data from given files, dir or file glob",
    license="GPL",
    keywords="yaml",
    url="https://github.com/ImmobilienScout24/yamlreader",
    requires=["yaml"],
    py_modules=[ "yamlreader" ],
    test_suite="test",
    package_dir={'':'src'},
    long_description="Small Python script that merges YAML files",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Programming Language :: Python",
        ],
     cmdclass={'clean' : completeClean},
     entry_points = {
    'console_scripts': [ 
        'yamlreader = yamlreader:__main',
        ]
}
)
