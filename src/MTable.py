#!/usr/bin/env ipython


"""A table is list of strings or list of lists. Allows reasonably flexible
querying mechanism"""


import sqlite3
import numpy as np
from datautils import columnize


#TODO. 
# Currently supports only named headers, plan to make completely generic
# Doesn not support deletion, insertion, etc, so good for one time use only 



class MTable():
    def __init__(self, tbl=None, tbltype='list', fields=None, fdtype=None):
        """constructs table for row/col access where,  
            tbl      => a list of rows, where each row is of 
            tbltype => a 'str' or 'list' (in quotes)
            fields   => fields specified if not part of the table, and must 
                        be in 'str' or 'list' format consistent w/tbltype"""
    
        self.con = None 
        self.cur = None
        self.tbl = []
        self.fields = []
        self.fdtype = []
        self.row_count = 0
        self.col_count = 0
        if tbl == None: 
            return  # no table constructed, only placeholder
        else:
            self.create_table(tbl, tbltype, fields, fdtype)


    def create_table(self, tbl=None, tbltype='list', fields=None, fdtype=None):
        """Actual table creation as part of constructor or overwriting stuff"""

        if self.con != None or self.cur != None:
            print """WARNING. No action taken since table already exists. Either
            clear table first or create a new Table object""" 
            return

        self.con = sqlite3.connect (':memory:')
        self.cur = self.con.cursor()

        if fields == None:        # table has embedded fields
            self.fields = tbl[0]
            self.tbl = tbl[1:] 
            self.row_count = len(tbl) - 1
        else:
            self.fields = fields
            self.tbl = tbl
            self.row_count = len(tbl) 

        if tbltype == 'list': pass
        elif tbltype == 'str': 
            self.fields = self.fields.strip().split()
            self.tbl = [r.strip().split() for r in self.tbl] 
        else: print "Unrecognized talbe type; please construct Table correctly"

        self.col_count = len(self.tbl[0])

        if fdtype == None:     self.fdtype = (" TEXT") * len(self.fields)
        elif tbltype == 'list': self.fdtype = tuple(fdtype)
        elif tbltype == 'str': self.fdtype = tuple(fdtype.strip().split())
   
        field_pair = []
        for f, fd in zip(self.fields, self.fdtype): 
            field_pair.append( f + ' ' + fd )
        field_pair = '(' + ' , '.join(field_pair) + ')'
        # print "field pair ",  field_pair 
        create_table_txt = "CREATE TABLE IF NOT EXISTS MemTable" + field_pair 
        print "Creating table with fields and data types =>", self.fields, self.fdtype
        self.cur.execute (create_table_txt)



        fields = '(' + ','.join(self.fields) + ')'
        fieldq = '(' + ','.join( ['?'] * len(self.fields) ) + ')'
        query = "INSERT INTO MemTable " + fields  + " VALUES " + fieldq
        self.cur.executemany(query, self.tbl) 



    def printall(self):
        """Print entire table"""
        if self.cur == None: return
        print "FULL TABLE:"
        self.cur.execute("""SELECT * FROM MemTable""")
        results = self.cur.fetchall()
        for r in results: print ' '*3, r


    def allrows(self, header=False):
        """Returns all rows from table - basically the whole table"""
        if header:
            self.tbl.insert(0,self.fields)
        return self.tbl


    def row(self, n, header=False):
        """Returns a single row from table starting with first row index as 0"""
        if self.cur == None: return
        if n >= len(self.tbl): return

        if header:
            return [self.fields, self.tbl[n]]
        else:
            return self.tbl[n] 


    def col(self, n, header=False):
        """Returns a single column from table with given header name""" 
        if self.cur == None: return
        if type(n) == str:  # ie, named acccess
            name = n
            # print "Returning column:",  name
            self.cur.execute("SELECT %s FROM MemTable" % (name))
            results = [r[0] for r in self.cur.fetchall()]
            if header:
                results.insert(0, name)
            return results 
        else:
            pass    # TODO. 


    def allcols(self, rtype='dict'):
        """Returns all columns from table in either dict form (default) or list form - 
            list form - allows column access as cols[4], cols[5] etc.
            dict form - allows column access as cols['Bid'] , cols['Ask'], etc.""" 

        if rtype == 'list':     # allows pure list like access
            cols = []
            for f in self.fields:
                cols.append( self.col(f) )
        elif rtype == 'dict':   # allows both indexed & dict access, not sequential
            cols = {} 
            for i, f in zip(range(len(self.fields)), self.fields):
                cols[i] = self.col(f)
                cols[f] = self.col(f)
        else: 
            print "ERROR. Return type must be specified as eiher 'list' or 'dict'"
        return cols


    def vector(self, n):
        """Returns a single column vector (ie, numpy array) from table; header is not an option""" 
        if self.cur == None: return
        if type(n) == str:  # ie, named acccess
            name = n
            self.cur.execute("SELECT %s FROM MemTable" % (name))
            results = [r[0] for r in self.cur.fetchall()]
            nresults = []
            for s in results: 
                if s == 'N/A' or s == 'NA':     # TODO. Missing data
                    print "WARNING. Missing data under column {%s}. Replacing with 0.0." % (name)
                    nresults.append(0.0)
                else:
                    nresults.append(s)

            try: nresults = np.array( [float(r) for r in nresults] )
            except ValueError: print "WARNING. Could not vectorize column to numpy array. Returning as list"
            except: print "ERROR. Could not vectorize column for some reason. Returning as list"
                
            return nresults 
        else:
            pass    # TODO. 


    def allvectors(self, rtype='dict'):
        """Returns all column vectors (numpy arrays) from table in either dict form (default) or list form - 
            list form - allows column access as vectors[4], vectors[5] etc.
            dict form - allows column access as vectors['Bid'] , vectors['Ask'], etc.""" 

        if rtype == 'list':     # allows pure list like access
            vectors = []
            for f in self.fields:
                vectors.append( self.vector(f) )
        elif rtype == 'dict':   # allows both indexed & dict access, not sequential
            vectors = {} 
            for i, f in zip(range(len(self.fields)), self.fields):
                vectors[i] = self.vector(f)
                vectors[f] = self.vector(f)
        else: 
            print "ERROR. Return type must be specified as eiher 'list' or 'dict'"
        return vectors


    def get_size(self):
        """Returns a tuple of row_count x col_count , ie (i, j) format eg:
        tbl.get_size() => (3,5) or 3 rows & 5 columns"""
        return self.row_count, self.col_count


    def insert(self, n, rowval):
        pass

    def delete(self, n):
        pass

    def replace(self, n, rowval):
        pass

    def clear(self):    
        """Clears out the table to free up memory & start afresh. Need to
        create_table() again after this command"""
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None





def test_table(tbl):
    # tblobj = MTable(tbl) # this will also work assumes all text
    tblobj = MTable(tbl, fdtype=["TEXT", "TEXT", "REAL", "REAL"])
    tblobj.printall()
    print 'row[1]:', tblobj.row(1)
    print 'row[3]:', tblobj.row(3, True)
    print 'col[Ask]:', tblobj.col('Ask')
    print 'col[Bid]:', tblobj.col('Bid', True)
    print 'all rows:', tblobj.allrows()
    print 'all columns:', tblobj.allcols()
    tblobj.clear()
    tblobj.printall()


def test_table2(newtbl):
    tblobj = MTable( newtbl, tbltype='str' ) 
    print 'row 1  :', tblobj.row(1) 
    print 'col Bid:', tblobj.col('Bid') 
    cols = tblobj.allcols()
    print cols['Last']
    print cols[4]
    print tblobj.vector('Ask'), "and type is ", type (tblobj.vector('Ask'))
    vectbl = tblobj.allvectors()
    for k,v in vectbl.items(): print "VECTOR[%s] = " % (k), v


def test_columnize(tbl):
    print 'WITHOUT HEADER' 
    for i,row in enumerate(columnize(tbl)): print 'COLUMN', i, row 
    print 'WITH HEADER' 
    for i,row in enumerate(columnize(tbl, False)): print 'COLUMN', i, row 


def pandas_table2(newtbl):
    import pandas as pd
    pd.DataFrame(newtbl)
    

if __name__ == '__main__': 
    Table2d = [ 
        ('Name', 'Date', 'Ask', 'Bid'),
        ('AAPL', '2013-05-15',  452.8, 451.7),
        ('TSLA', '2013-06-14',  150.2, 149.6),
        ('ACMP', '2013-08-10',   57.3,  56.6),
        ('JCP' , '2013-07-19',    7.5,   7.3),
        ('MA'  , '2013-09-07',  221.1, 220.6)
        ]
    test_table(Table2d)


    newtbl = ['Ticker  Strike C_P  Exp           Last     Bid     Ask', 
            u'GDOT    22.5    C 2014-02-22     2.7     3.2     3.5', 
            u'GDOT    25.0    C 2014-02-22    1.64     1.7    1.95', 
            u'GDOT    30.0    C 2014-02-22    0.49    0.25     0.5']
    test_table2(newtbl)
    test_columnize(Table2d)

