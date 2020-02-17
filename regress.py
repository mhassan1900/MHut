#!/usr/bin/env python

from __future__ import print_function 

#import unittest as ut
import sys
import mhut.testutils as testutils
from testdir.TestDatautils import TestDatautils
from testdir.TestTimeutils import TestTimeutils

project = 'mhut'
test_suites = [TestDatautils, TestTimeutils]
grand_summary = {}

for ts in test_suites:
    tsummary, dummy = testutils.run_tests(ts)
    grand_summary = testutils.append_summary(grand_summary, tsummary)

print ("#" * 80)
print ("# REGRESSION RESULTS UNDER 'project #".format(project))
print ("#" * 80)

testutils.print_summary(grand_summary, "GRAND SUMMARY")
print ("#" * 80)
