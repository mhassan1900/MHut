#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user

# -- Standard boilerplate header - begin
import unittest as ut
import sys, os
from os.path import abspath, dirname

cdir = dirname(abspath(sys.argv[0]))        # testdir 
pdir = dirname(cdir)                        # 
srcdir = os.path.join(pdir, 'src')
sys.path.insert(0, srcdir)

pathlist = []
for p in sys.path:
    if not p in pathlist: pathlist.append(p)
sys.path = pathlist

from testutils import run_tests, twrap
# -- Standard boilerplate header - end 
import pandas as pd
import numpy as np
from datautils import filter_column, columnize 


class TestDatautils(ut.TestCase):

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

    @twrap
    def test_filter_column(self):
        df  = pd.DataFrame(100*np.random.rand(12).reshape(4,3), columns=list('ABC'))
        df1 = df.copy() 
        df1.index  = [10, 10.25, 10.5, 10.75]  
    
        self.assertTrue(df.ix[1].equals(           filter_column(df, '1')))
        self.assertTrue(df.ix[1:3].equals(         filter_column(df, '1:3')))
        self.assertTrue(df.ix[:2].equals(          filter_column(df, ':2')))
        self.assertTrue(df.ix[2:].equals(          filter_column(df, '2:')))
        self.assertTrue(df[df.index<2].equals(     filter_column(df, '<2')))
        self.assertTrue(df[df.index <= 1].equals(  filter_column(df, '<=1')))
        self.assertTrue(df[df.index != 1].equals(  filter_column(df, '!=1')))
        self.assertTrue(df[(df.index > 1) & (df.index <= 2)].equals(   
                            filter_column(df, '>1 & <=2')))

        self.assertTrue(df1.ix[10.5].equals(              filter_column(df1, '10.5')))
        self.assertTrue(df1.ix[10.25:10.5].equals(        filter_column(df1, '10.25:10.5')))
        self.assertTrue(df1.ix[:10.5].equals(             filter_column(df1, ':10.5')))
        self.assertTrue(df1.ix[10.5:].equals(             filter_column(df1, '10.5:')))
        self.assertTrue(df1[df1.index >= 10.5].equals(    filter_column(df1, '>=10.5')))
        self.assertTrue(df1[df1.index == 10.25].equals(   filter_column(df1, '==10.25')))
        self.assertTrue(df1[(df1.index < 10.25) | (df1.index >= 10.75)].equals(
                 filter_column(df1, '<10.25 | >=10.75')))

        # expect errors
        self.assertTrue(len(filter_column(df, '1.0'))==0) # ERROR (returns empty table)
        self.assertTrue(len(filter_column(df1, '1'))==0)  # ERROR (returns empty table)


    @twrap
    def test_columnize(self):
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


