#!/usr/bin/env python
# Run as:
# python setup.py install [--user needed if no root permissions or virtual env]


import sys
import os

sys.path.insert(0, os.getcwd())  

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL
from setuptools import setup, find_packages
import mhut 


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    # name="mhut-mhassan1900", 
    name="mhut",
    version = mhut.__version__,
    author='Mahmud Hassan',
    author_email='mhassan1900@users.noreply.github.com',
    description='Various utilities by MH that show up often in project use',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mhassan1900/mhut",
    project_urls={
        "Bug Tracker": "https://github.com/mhassan1900/mhut/issues",
    },
    scripts = ['scripts/pathutils'],
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",
    #    "Operating System :: OS Independent",
    #],
    # package_dir={"": "src"},
    # packages=find_packages(where="src"),
    packages = find_packages(exclude=('testdir',)),
    python_requires=">=3.7",
    py_modules = ['testutils', 'timeutils', 'datautils', 'profutils', 'pathutils'],
)



# Last version - for reference
# 
#   setup(
#       name = 'mhut',   
#       version = mhut.__version__,
#       author = 'Mahmud Hassan',
#       author_email = 'mhassan1900@users.noreply.github.com',
#       description='Various utilities by MH that show up often in his use',
#       scripts = ['scripts/pathutils'],
#       packages = find_packages(exclude=('testdir',)),
#       py_modules = ['testutils', 'timeutils', 'datautils', 'profutils', 'pathutils']
#   )
