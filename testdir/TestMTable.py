#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user

# -- Standard boilerplate header - begin
import unittest as ut
import sys, os
from os.path import abspath, dirname

cdir = dirname(abspath(sys.argv[0]))        # testdir 
pdir = dirname(cdir)                        # AIquotes 
quotes_dir = os.path.join(pdir, 'aiquotes')
sys.path.insert(0, quotes_dir)

pathlist = []
for p in sys.path:
    if not p in pathlist: pathlist.append(p)
sys.path = pathlist

from testutils import run_tests, dbexec_cmd, dbexec_scr, dbpopulate_testoptions
# -- Standard boilerplate header - end 


# NOTE. it is a problem if we import individual functions
# because of a global (static) var or two
import numpy as np

from MTable import columnize





class TestMTable(ut.TestCase):

    # globally available data struct
    @classmethod
    def setUpClass(cls):
        print "class setUp - Nothing to do" 

    @classmethod
    def tearDownClass(cls):
        print "class tearDown - Nothing to do" 


    # applied per method in class 
    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_columnize(self):
        print "-- Running test: <test_columnize> --\n"
        tbl = [['Strike', 'Bid',  'Ask'],
               [73.0 ,  2.65, 2.70],
               [73.5 ,  2.47, 2.52],
               [74.0 ,  2.30, 2.36]]

        xpct = [[73.0, 73.5, 74.0],
                [2.65, 2.47, 2.30],
                [2.70, 2.52, 2.36]]
        result = columnize(tbl, True) # strip_header
        result = [list(r) for r in result]  # convert back from np.array to list
        self.assertEqual(xpct, result)

        # TODO. N/A's are not handled gracefully
        #tbl[3][1] = 'N/A' # 2.3 -> 'N/A'
        #result = vectorize(tbl) 
        # self.assertEqual(xpct, result) 


if __name__ == '__main__':
    # ut.main()
    run_tests(TestMTable)


