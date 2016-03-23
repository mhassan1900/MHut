DESCRIPTION
===========

Various utilities I found useful that are needed on a regular basis.
Not really meant to be specific to any project. Just stuff that comes up
on a regular basis.

Also the dumping ground for a bunch of various utils that don't fit
anywhere.

Offers following modules for import:

*  mhut.msgutils  - Messaging & printing utils; very simple stuff and alternative to logging
*  mhut.testutils - Testutils is needed for regression reporting. Convenient set of
                    functions for pretty reporting & such
*  mhut.pathutils - convenience module for manipulating environment variables

Following scripts will available after installation:
  pathutils       - This is a copy of pathutils.py and can be executed standalone



INSTALLATION
============

To install type:

$ make install

Run setup.py with appropriate modifications. By default, this is installed in the user's
site-package directory.

The script "pathutils" is installed under Python2.7/bin directory.

To uninstall, type:

$ make uninstall

NOTE. For the user directory, error messages may appear, but the 'egg' package will be gone.



RELEASE HISTORY
===============

MHut-1.3.0   Mar 21, 2016   
--------------------------
- Renamed MHutils to MHut to avoid conflict w/existing package on PyPy
- Removed MTable
- Instead of installing individual modules, now installs the utils under the umbrella of mhut
- Cleaned up db related stuff from here
- Added pathutils as convenience module as well as script

MHutils-1.2.0   Jan 22, 2016   
----------------------------
Primarily corrections for removing deprecated warning messages after upgrading
pandas to v0.17.


MHutils-1.1.0   Nov 24, 2014
----------------------------
Added datautils for extra functionality to tackon on numpy & pandas.

Offers following additional module for import:

* datautils             


MHutils-1.0.0   Oct 23, 2014
----------------------------
First release for multi-project use.

Offers following modules for import:

* msgutils  - Messaging & printing utils
* testutils - Testutils is needed for regression reporting. Convenient set of
              functions for pretty reporting & such
* MTable    - My own class for working w/2D tables. Not as sophisticated as pandas
              but sometimes more convenient & faster for small stuff.
