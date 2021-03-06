#!/usr/bin/env python2.7
# Run as:
# python setup.py install --user

# -- Standard boilerplate header - begin
import unittest as ut
import sys, os
from os.path import abspath, dirname
from os.path import join as osjoin

cdir = dirname(abspath(__file__))   # sys.argv[0])) = # testdir
pdir = dirname(cdir)                #
srcdir = osjoin(pdir, 'mhut')
sys.path.insert(0, srcdir)

pathlist = []
for p in sys.path:
    if not p in pathlist: pathlist.append(p)
sys.path = pathlist

from testutils import run_tests, twrap
# -- Standard boilerplate header - end
import pandas as pd
import numpy as np
from datautils import *


# -- golden dataset --
G_dict = {
    'Name'        : ['A Cat', 'A Dog', 'Neither'],
    'my r2'       : [ 1,      0,        0],
    'my d2'       : [ 1,      0,        0],
    'other piper' : [ 0,      4,        0],
    'solomon'     : [ 0,      0,        2]}
G_DF = pd.DataFrame.from_dict( G_dict, orient='index')
G_DF.drop('Name', inplace=True)
G_DF.index.name = 'Name'
G_DF.columns = G_dict['Name']
G_DF = G_DF.reindex(['my r2', 'my d2', 'other piper', 'solomon'])
for c in G_DF.columns: G_DF[c] = pd.to_numeric(G_DF[c])


G1_dict = {    # I      II        III       IV        V
    'a': [2.071527, 1.998107, 2.029159, 1.192129, 1.459613],
    'b': [1.465882, 1.242207, 2.122667, 1.587954, 1.842492],
    'c': [1.505012, 1.674715, 1.436381, 1.626080, 1.435298],
    'd': [2.121946, 2.005520, 2.115850, 1.795292, 2.076429]
}
G1_DF = pd.DataFrame.from_dict(G1_dict, orient='index')
G1_DF.columns = 'I II III IV V'.split()

# -- convenience datasets for checking results --
G1_dict_R0 = {
    'a': [2.0, 2.0, 2.0, 1.0, 1.0], 'b': [1.0, 1.0, 2.0, 2.0, 2.0],
    'c': [2.0, 2.0, 1.0, 2.0, 1.0], 'd': [2.0, 2.0, 2.0, 2.0, 2.0]
}
G1_DF_R0 = pd.DataFrame.from_dict(G1_dict_R0, orient='index')
G1_DF_R0.columns = G1_DF.columns

G1_dict_R2 = {
    'a': [2.07, 2.00, 2.03, 1.19, 1.46],
    'b': [1.47, 1.24, 2.12, 1.59, 1.84],
    'c': [1.51, 1.67, 1.44, 1.63, 1.44],
    'd': [2.12, 2.01, 2.12, 1.80, 2.08]
}
G1_DF_R2 = pd.DataFrame.from_dict(G1_dict_R2, orient='index')
G1_DF_R2.columns = G1_DF.columns





class TestDatautils(ut.TestCase):

    # globally available data struct
    @classmethod
    def setUpClass(cls):
        print("class setUp - Nothing to do")

    @classmethod
    def tearDownClass(cls):
        print("class tearDown - Nothing to do")


    # applied per method in class
    def setUp(self):
        pass

    def tearDown(self):
        pass

    ## --------------------------------------------------------------------- ##
    @twrap
    def test_filter_column(self):
        df  = pd.DataFrame(100*np.random.rand(12).reshape(4,3), columns=list('ABC'))
        df1 = df.copy()
        df1.index  = [10, 10.25, 10.5, 10.75]

        self.assertTrue(df.iloc[1].equals           (filter_column(df, '1')))
        self.assertTrue(df.iloc[1:4].equals         (filter_column(df, '1:3')))
        self.assertTrue(df.iloc[:3].equals          (filter_column(df, ':2')))
        self.assertTrue(df.iloc[2:].equals          (filter_column(df, '2:')))
        self.assertTrue(df[df.index<2].equals       (filter_column(df, '<2')))
        self.assertTrue(df[df.index <= 1].equals    (filter_column(df, '<=1')))
        self.assertTrue(df[df.index != 1].equals    (filter_column(df, '!=1')))
        self.assertTrue(df[(df.index > 1) & (df.index <= 2)].equals(
                            filter_column(df, '>1 & <=2')))

        self.assertTrue(df1.loc[10.5].equals           (filter_column(df1, '10.5')))
        self.assertTrue(df1.loc[10.25:10.5].equals     (filter_column(df1, '10.25:10.5')))
        self.assertTrue(df1.loc[:10.5].equals          (filter_column(df1, ':10.5')))
        self.assertTrue(df1.loc[10.5:].equals          (filter_column(df1, '10.5:')))
        self.assertTrue(df1[df1.index >= 10.5].equals   (filter_column(df1, '>=10.5')))
        self.assertTrue(df1[df1.index == 10.25].equals  (filter_column(df1, '==10.25')))
        self.assertTrue(df1[(df1.index < 10.25) | (df1.index >= 10.75)].equals(
                 filter_column(df1, '<10.25 | >=10.75')))

        # expect errors in some version of pandas
        self.assertTrue(df.iloc[1].equals           (filter_column(df, '1.0')))
        # self.assertTrue(filter_column(df, '1.0') - df.iloc[1]) # 1.0 => 1 (returns non-empty table)


    ## --------------------------------------------------------------------- ##
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



    ## --------------------------------------------------------------------- ##
    @twrap
    def test_R2(self):
        self.assertEqual(4.00,  R2(4))
        self.assertEqual(4.50,  R2(4.5))
        self.assertEqual(4.58,  R2(4.58))
        self.assertEqual(4.59,  R2(4.586))
        self.assertEqual(4.58,  R2(4.584))

    ## --------------------------------------------------------------------- ##
    @twrap
    def test_R3(self):
        self.assertEqual(4.000,  R3(4))
        self.assertEqual(4.500,  R3(4.5))
        self.assertEqual(4.585,  R3(4.585))
        self.assertEqual(4.586,  R3(4.5863))
        self.assertEqual(4.587,  R3(4.5867))

    ## --------------------------------------------------------------------- ##
    @twrap
    def test_RN(self):
        self.assertEqual(4.00,     RN(4))
        self.assertEqual(4.57,     RN(4.5736))
        self.assertEqual(4.527,    RN(4.5268, 3))
        self.assertEqual(4.57360,  RN(4.5736, 5))
        self.assertEqual('abc',    RN('abc', 4))

    ## --------------------------------------------------------------------- ##
    @twrap
    def test_roundoff_list(self):
        alist = [ 2.5768, 'bee', 256]
        roundoff_list(alist, 3)
        self.assertEqual([2.577, 'bee', 256.000], alist)

        alist = [ 2.5768, 'bee2', 256]
        roundoff_list(alist)
        self.assertEqual([2.58, 'bee2', 256.00], alist)


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_roundoff_dict(self):
        adict = {'A': 2.576, 'B': 'bee', 'C': 256, 'D': [32.1475, 32, 'fee']}
        roundoff_dict(adict, 3)
        axpct = {'A': 2.576, 'B': 'bee', 'C': 256.000, 'D': [32.148, 32.000, 'fee']}
        self.assertEqual(axpct, adict)

        adict = {'A': 2.576, 'B': 'bee', 'C': 256, 'D': [32.1475, 32, 'fee']}
        roundoff_dict(adict, 2)
        axpct = {'A': 2.58, 'B': 'bee', 'C': 256.00, 'D': [32.15, 32.00, 'fee']}
        self.assertEqual(axpct, adict)


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_isnumeric(self):
        self.assertTrue(isnumeric(23))
        self.assertTrue(isnumeric(23.57))
        self.assertTrue(isnumeric('.57'))
        self.assertTrue(isnumeric('257'))
        self.assertFalse(isnumeric('257.a'))
        self.assertFalse(isnumeric('a.bc'))
        self.assertFalse(isnumeric('a.25bc'))
        self.assertFalse(isnumeric('1.25.37'))


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_reorder_list(self):
        orig_list = ['apple', 'banana', 'cantaloupe', 'guava', 'mango']
        des_order = ['banana', 'guava']

        new_list = reorder_list(orig_list, des_order) # , 'any'
        b_ix = new_list.index('banana')
        g_ix = new_list.index('guava')
        self.assertEqual(1, g_ix-b_ix)
        self.assertEqual(set(orig_list), set(new_list))
        self.assertNotEqual(orig_list, new_list)

        new_list = reorder_list(orig_list, des_order, 'begin')
        self.assertEqual(new_list, 'banana guava apple cantaloupe mango'.split())

        new_list = reorder_list(orig_list, des_order, 'end')
        self.assertEqual(new_list, 'apple cantaloupe mango banana guava'.split())

        new_list = reorder_list(orig_list, des_order, 'before')
        self.assertEqual(new_list, 'apple cantaloupe banana guava mango'.split())

        new_list = reorder_list(orig_list, des_order, 'after')
        self.assertEqual(new_list, 'apple banana guava cantaloupe mango'.split())

        new_list = reorder_list(orig_list, 'mango cranberry cantaloupe'.split())
        m_ix = new_list.index('mango')
        c_ix = new_list.index('cantaloupe')
        self.assertEqual(1, c_ix-m_ix)
        self.assertEqual(set(orig_list), set(new_list))

        des_order = 'banana apple cantaloupe something_else mango guava'.split()
        new_list = reorder_list(orig_list, des_order)
        self.assertEqual(new_list, ['banana', 'apple', 'cantaloupe', 'mango', 'guava'])

    ## --------------------------------------------------------------------- ##
    @twrap
    def test_df_reorder_columns(self):
        A,B,C,D,E = 0,1,2,3,4
        m = np.random.rand(30).reshape(6,5)
        df = pd.DataFrame( m, columns=list('ABCDE') )

        df1 = df_reorder_columns(df, orderlist=list('CDAEB'))
        m_xpdf = np.array(list(zip(m[:,C],m[:,D],m[:,A],m[:,E],m[:,B])))
        xpdf1 = pd.DataFrame( m_xpdf, columns=list('CDAEB') )

        df2 = df_reorder_columns(df, list('BD'),'begin')
        m_xpdf2 = np.array(list(zip(m[:,B],m[:,D],m[:,A],m[:,C],m[:,E])))
        xpdf2 = pd.DataFrame( m_xpdf2, columns=list('BDACE') )

        df3 = df_reorder_columns(df, list('CFA'),'end')
        m_xpdf3 = np.array(list(zip(m[:,B],m[:,D],m[:,E],m[:,C],m[:,A])))
        xpdf3 = pd.DataFrame( m_xpdf3, columns=list('BDECA') )

        self.assertTrue(df1.equals(xpdf1))
        self.assertTrue(df2.equals(xpdf2))
        self.assertTrue(df3.equals(xpdf3))


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_txt2df(self):

        alltxt = '''
                   |      |          |
        Name        A Cat       A Dog Neither
        my r2         1        0        0
        my d2         1        0        0

        other piper     0        4        0
        solomon       0        0        2

        '''
        df = txt2df(alltxt)
        for c in df.columns: df[c] = pd.to_numeric(df[c])
        self.assertTrue(G_DF.equals(df))


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_parse2df(self):
        df = parse2df(osjoin(cdir, 'test_parse2df.txt'))
        for c in df.columns: df[c] = pd.to_numeric(df[c])
        self.assertTrue(G_DF.equals(df))


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_broadcast(self):
        alist = [1,2,3,4]
        aa = np.array(alist)
        ma = np.matrix(alist)
        sa = pd.Series(alist)

        # -- check lists --
        x = broadcast(alist, 3, 0)
        y = broadcast(alist, 3)

        xpct_x = [alist, alist, alist]
        xpct_y = [[1,1,1], [2,2,2], [3,3,3], [4,4,4]]
        self.assertEqual( xpct_x, x)
        self.assertEqual( xpct_y, y)

        # -- check arrays  --
        x = broadcast(aa, 3, 0)
        y = broadcast(aa, 3)

        xpct_x = np.array( [alist, alist, alist] )
        xpct_y = np.array( [[1,1,1], [2,2,2], [3,3,3], [4,4,4]] )
        self.assertEqual( (xpct_x-x).sum(), 0)
        self.assertEqual( (xpct_y-y).sum(), 0)

        # -- check matrices  --
        x = broadcast(ma, 3, 0)
        y = broadcast(ma, 3)

        xpct_x = np.matrix( [alist, alist, alist] )
        xpct_y = np.matrix( [[1,1,1], [2,2,2], [3,3,3], [4,4,4]] )
        self.assertEqual( (xpct_x-x).sum(), 0)
        self.assertEqual( (xpct_y-y).sum(), 0)

        # -- check series  --
        x = broadcast(sa, 3, 0)
        y = broadcast(sa, 3)

        xpct_x = pd.DataFrame( [alist, alist, alist], dtype=float )
        xpct_y = pd.DataFrame( [[1,1,1], [2,2,2], [3,3,3], [4,4,4]], dtype=float )
        self.assertTrue( xpct_x.equals(x) )
        self.assertTrue( xpct_y.equals(y) )


    ## --------------------------------------------------------------------- ##
    @twrap
    def test_roundoff_df(self):

        df = roundoff_df(G1_DF)
        self.assertTrue(df.equals(G1_DF_R0))

        df = roundoff_df(G1_DF, 2)
        self.assertTrue(df.equals(G1_DF_R2))


        df = roundoff_df(G1_DF, 2, columns=['III', 'V'])
        G1_rounded = G1_DF.copy()
        G1_rounded.reindex( list('abcd') )     # becomes acbd for some reason
        G1_rounded['III'] =  pd.Series(dict(list(zip(list('abcd'), [2.03, 2.12, 1.44, 2.12] ))))
        G1_rounded['V']   =  pd.Series(dict(list(zip(list('abcd'), [1.46, 1.84, 1.44, 2.08] ))))
        self.assertTrue(df.equals(G1_rounded))


        df = roundoff_df(G1_DF, 2, indices=['b', 'd'])
        G1_rounded = G1_DF.copy()
        G1_rounded.loc['b'] = [1.47, 1.24, 2.12, 1.59, 1.84]
        G1_rounded.loc['d'] = [2.12, 2.01, 2.12, 1.80, 2.08]
        self.assertTrue(df.equals(G1_rounded))

        df = roundoff_df(G1_DF, 2, columns=['III', 'V'], indices=['b', 'd'])
        G1_rounded = G1_DF.copy()
        G1_rounded.loc['b', ['III', 'V']] = [2.12, 1.84]
        G1_rounded.loc['d', ['III', 'V']] = [2.12, 2.08]
        self.assertTrue(df.equals(G1_rounded))



if __name__ == '__main__':
    # ut.main()
    run_tests(TestDatautils)
