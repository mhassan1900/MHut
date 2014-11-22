#!/usr/bin/env python2.7

import unittest as ut
import sys
sys.path.append( 'src' ) 

pathlist = []
for p in sys.path: 
    if not p in pathlist: pathlist.append(p)
sys.path = pathlist 

for p in sys.path: print " --> ", p


import testutils
from testdir.TestMTable import TestMTable

test_suites = [TestMTable]
grand_summary = {}


for ts in test_suites: 
    tsummary, dummy = testutils.run_tests(ts)
    grand_summary = testutils.append_summary(grand_summary, tsummary) 

print "#" * 70
print "# REGRESSION RESULTS UNDER 'aiquotes' #"
print "#" * 70

testutils.print_summary(grand_summary, "GRAND SUMMARY")
print "#" * 70


