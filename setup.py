#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user

#from distutils.core import setup   - DO NOT USE; DUMPS EVERTYHING UNDER SITE-PACKAGES & UNCLEAN INSTALL  

from setuptools import setup

setup(name='MHutils',   # best to have same names as main source file
      # author='Mahmud Hassan',
      # author_email='mahmud.hassan@gmail.com',
      # scripts = ['scripts/dupfinder_gui.py'],
      version='1.0.0',
      description='Various utilities that show up often',
      package_dir = {'': 'src'},     
      py_modules=['MTable', 'msgutils', 'testutils', 'datautils']    
)

