#!/usr/bin/env python2.7

'''Data structure utils module for generic use. Has functions
   that would be really nice to add to string, dictionary or 
   DataFrame types. Could extend some of these to add capability 
'''
import re
import pandas as pd
import numpy as np 
import logging 
import datetime as dt


_ANYOP_ = re.compile(r'[><=&|]')
logger = logging.getLogger(__name__)




## ------------------------------------------------------------------- ##
def R2(num):
    """Simple round off to 2 dec places wrapper"""
    return round(num, 2)

## ------------------------------------------------------------------- ##
def R3(num):
    """Simple round off to 3 dec places wrapper"""
    return round(num, 3)

## ------------------------------------------------------------------- ##
def RN(num, places=2):
    """Simple round off to 2 dec places by default wrapper. Fails silently 
    on non floats"""
    try: f = round(num, places)
    except: f = num
    return f 

## ------------------------------------------------------------------- ##
def roundoff_list(alist, places=2):
    """Rounds off contents in a list to '2' places by default.  Fails 
    silently on non floats.  NOTE. list is modified INPLACE"""
    for i, v  in enumerate(alist): 
        alist[i] = RN(v, places) 
    return  

## ------------------------------------------------------------------- ##
def roundoff_dict(adict, places=2):
    """Rounds off contents in a dictionary table to '2' places by default.
    Can handle one level deep of list of nums. Fails silently on non floats.
    NOTE. Dictionary is modified INPLACE"""
    for k,v  in adict.items(): 
        if type(v) == list: roundoff_list(v, places)
        else: adict[k] = RN(v, places)
            # v = [round(f, places) for f in v]
        #try: adict[k] = round(v, places)
        #except: continue # silenty move on 
    return  


## ------------------------------------------------------------------- ##
def isnumeric(a):
    """Returns True if 'a' is an int, float, or a string that could be converted
    to an int or float"""
    if type(a) == int or type(b) == float: return True
    elif type(a) == str:
        if a.replace('.','').isdigit() and a.count('.') < 2: 
            return True
    elif np.dtype(a) == int or np.dtype(b) == float: return True
    return False


## ------------------------------------------------------------------- ##
def pprint_dict(adict, orderlist=[]):
    """Prints out a dictionary (eg stock quote) nicely in desired print orderlist."""

    if adict == {}: return
    keyset = set(adict.keys())
    orderset = set(orderlist)
    if not orderset.issubset(keyset): 
        logger.warn( "Specified order is mismatched. Bad fields will be ignored")
        for k in orderset: 
            if k not in keyset: orderlist.remove(k)
    
    # now print in clean order
    remainset = keyset.symmetric_difference(orderlist)
    maxlen = max( [len(k) for k in keyset] ) 

    printsets = orderlist + list(remainset)
    for k in printsets: 
        v = adict[k]
        if type(v) == pd.Series or type(v) == pd.DataFrame: 
            print '-' * 80
            print v
            print '-' * 80
            continue
        if type(v) == dt.datetime: v = dt.datetime.ctime(v)
        print k.ljust(maxlen), ':', v 
    

## ------------------------------------------------------------------- ##
def reorder_list(origlist, orderlist, qualifier='any'):
    """
    origlist: Given list of labels eg: ['Strike', 'Exp', 'Ask', 'Bid'] 
    orderlist: List of labels in desired order, eg: ['Exp', 'Strike'] 
    qualifier: One of ['any'|'before'|'after'|'begin'|'end']
        any - any position as longer as order is satisfied
        before - insert labels before position of the last entry
        after - insert labels after position of first entry
        begin - set the order to beginning of list of all labels
        end - set the order to end of the list of all labels
    NOTE1. origlist is expected to have UNIQUE entries ONLY 
    NOTE2. All positions of given orderlist will be adjacent to each other."""

    
    if len(origlist) < 2: return origlist 
    if len(orderlist) < 2: return  origlist
    keylist = origlist[:]

    keyset = set(keylist)
    orderset = set(orderlist)
    if not orderset.issubset(keyset): 
        logger.warn( "Specified order is mismatched. Bad fields will be ignored")
        for k in orderset: 
            if k not in keyset: orderlist.remove(k)

    
    if qualifier in ('any', 'after'):   # currently the same
        idx = keylist.index(orderlist[0])
        for k in orderlist: keylist.remove(k)
        keylist = keylist[:idx] + orderlist + keylist[idx:]
    if qualifier == 'before':
        idx = keylist.index(orderlist[-1])
        for k in orderlist: keylist.remove(k)
        keylist = keylist [:idx] + orderlist + keylist[idx:]
    if qualifier == 'begin':
        for k in orderlist: keylist.remove(k)
        keylist = orderlist + keylist 
    if qualifier == 'end':
        for k in orderlist: keylist.remove(k)
        keylist = keylist + orderlist 
    
    return keylist



## ------------------------------------------------------------------- ##
def df_reorder_columns(df, orderlist=[], qualifier='any'):
    """Sets the order of columns of a dataframe in desired order.
    Note that behavior of qualifier is same as reorder_list() function. 
    """

    keylist = reorder_list(list(df.columns), orderlist, qualifier) 
    return df.reindex_axis(keylist, axis=1)


# --------------------------------------------------------------- #
def filter_column(df, qr, col=None):
    """Filters out indices from an a DataFrame using the same 
    symantics as DataFrame indexing, and returns a new DataFrame
        df: DataFrame input (unmodified)
        qr: Simple query string that supports following forms:
              int, float, range, relational, unary & binary logical ops 
        col: if None, applies the query on the index, else matching col
    Eg, qr could be: 2, 2:3, <1, !=2, 10.5:10.75, <3 | >5, >7 & <8  
    They ALL MUST be strings though.
    Returns a an empty DataFrame if it fails.
    """
    opset = _ANYOP_.findall(qr)
    inner_eval = False
    col = 'index' if col==None else col

    if opset: 
        inner_eval = True
        if '&' in opset:
            qs = qr.split('&')
            qs = '(df.{} {}) & (df.{} {})'.format(col, qs[0], col, qs[1])
        elif '|' in opset:
            qs = qr.split('|')
            qs = '(df.{} {}) | (df.{} {})'.format(col, qs[0], col, qs[1])
        else:
            print 'how about here'
            qs = '(df.{} {})'.format(col, qr) 
            print qs
    else:
        if col == 'index':
            qs = 'df.ix[{}]'.format(qr) 
        else:
            logger.error("Could not process evaluation of '{}. Returning empty DF'".format(qs))
            return pd.DataFrame( {} ) 

    logger.debug('Evaluating {}'.format(qs)) 

    try:
        dfout = df[eval(qs)] if inner_eval else eval(qs)
    except:
        logger.error("Could not process evaluation of '{}. Returning empty DF'".format(qs))
        dfout = pd.DataFrame( {} ) 

    return dfout # either a dataframe or a series


## ------------------------------------------------------------------- ##
def columnize(tbl, strip_header=True):   
    """Wrapper for converting a table in list of row (vector) format into list of column 
    (vector) format by slicing it. M rows of N-elem list/tuple would return N-rows of M-elem
    lists eg:  100 rows x (1x3) tuples => 3 rows of (100x1) vectors. So:
        
    [['Strike', 'Bid',  'Ask',    [np.array(73.0, 73.5, 74.0),
     [73.0 ,  2.65, 2.70,      =>  np.array(2.65, 2.47, 2.30), 
     [73.5 ,  2.47, 2.52,          np.array(2.70, 2.52, 2.36)]
     [74.0 ,  2.52, 2.36]]         
     NOTE the conversion of floats to strs in the transposed format is not kept by
     default IF the header is included ie, strip_header=False. Some massaging needed then. 
     """

    #for i in range(len(tbl[1:])):
    #    for j in range(len(tbl[i])):
    #        if tbl[i][j] == 'N/A': tbl[i][j] = np.NaN 

    if len(tbl)==0 or (len(tbl)==1 and strip_header): 
        logger.error('Empty table entered. No action taken') 
        return []

    if strip_header: amat = np.matrix( tbl[1:] )    # MUST be a consistent 2-D table
    else: amat = np.matrix( tbl )    

    # n=inject to preserve native data types - except int->float
    row_types = [type(a) for a in tbl[1]]
    row_types = [float if a==int else a for a in row_types] 
     
    clist = amat.transpose().tolist()
    return [np.array(c, dtype=ntype) for c,ntype in zip(clist,row_types)] 


## ------------------------------------------------------------------- ##



def parse2df(fname):
    '''Returns & generates a DataFrame from a file that has free from
    spacing BUT has the header position specified with "|". Currently not
    changeable but may be modified in the future. Helps deal with non-CSV
    format but that has maligned tabs and spaces. '''

    # NOTE. This is currently done in two passes to make use of exisiting 
    # function txt2df & is a little slow, but ok for small files to parse

    try:
        fin = open (fname)
    except:
        print "Could not open {} for reading!".format(fname)

    txtlist = fin.readlines()    # slurp whole thing
    fin.close()
  
    sep_pragma = '#<pr:sep>'
    txtlist = [t.replace(sep_pragma,' '*len(sep_pragma)) if t.lstrip().startswith(sep_pragma) else t 
                for t in txtlist]
    df = txt2df(''.join(txtlist), header_sep='|', header=True, skip_comment=True, index='default')
    return df




## ------------------------------------------------------------------- ##

def txt2df(strtxt, header_sep='|', header=True, skip_comment=True, index='default'):
    '''Returns & generates a DataFrame from a string that has free form
    spacing BUT has the header position specified with "|". Currently not
    changeable but may be modified in the future. Helps deal with non-CSV
    format but that has maligned tabs and spaces. 
        strtxt:       blob of text that needs to be parsed 
        header:       [True|False] - has a header or not 
        header_sep:   character marking positions of string separation  
        skip_comment: [True|False] - determine if comments are to be skipped
                      over. Empty lines are always ignored. 
                      currently only '#' is treated as comment 
        index:        use 'default', None, or any other valid column 
    '''

    positions = []
    lol = []

    sep_found = False 

    for line in strtxt.split('\n'):
        if len(line.strip()) == 0:  # skip blank
            continue
        elif not sep_found and line.lstrip().startswith(header_sep): 
            positions = [i for (i, c) in enumerate(line) if c == header_sep]
            continue
        elif (line.lstrip()).startswith('#'):   # skip comment 
            continue

        line = line.replace('\t', ' ')

        if len(positions) == 0: # use split by space by default, basically csv type
            lol.append( line.strip().split() )
        else:
            startpos = [0] + positions[:]
            endpos = positions[:] + [len(line)]
            # print 'S:', startpos  # DEBUG
            # print 'E:', endpos 
            tmp = [line[a:b].strip() for a,b in zip(startpos,endpos)]
            # print tmp 
            lol.append(tmp)


    index_name = lol[0][0] if index == 'default' else index

    df = pd.DataFrame(lol[1:], columns =lol[0])
    df = df.convert_objects(convert_numeric=True) 

    if index_name != None:
        df.set_index(index_name, inplace=True)
    return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    df = parse2df('test_parse2df.txt')
    print df

