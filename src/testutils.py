#!/usr/bin/env python2.7

'''Tests utils module for ease of running & integrating test results.
   Execute this function instead of the standard ut.main(), eg:
        run_tests(TestTimeutils)
'''

import unittest as ut
import sqlite3


# ------------------------------------------------------------ #
def twrap(func):
    """Decorator for test functions to print out what test is being run"""
    def inner(*args):
        print "-- Running test: <{}> --\n".format(func.__name__) 
        return func(*args)
    return inner


# ------------------------------------------------------------ #
def run_tests(test_case):
    loader = ut.TestLoader().loadTestsFromTestCase(test_case)
    result = ut.TestResult()
    loader(result)
    print "=" * 60
    print "TEST RESULTS FOR", test_case.__name__ 
    
    print "*FAILURES*"
    print "-" * 60

    for t, f in result.failures: 
        print "->", t, "<-"
        print f 
    for t, e in result.errors: 
        print "->", t, "<-"
        print e 

    print "*ERRORS*"
    print "-" * 60

    tcount = result.testsRun
    fcount = len(result.failures)
    ecount = len(result.errors)
    pcount = tcount - fcount - ecount
    prate = round( 100.0* pcount/float(tcount), 2)

    summary = {}
    summary['Name'       ] = test_case.__name__ 
    summary['Pass'       ] = pcount 
    summary['Failures'   ] = fcount 
    summary['Errors'     ] = ecount 
    summary['Total'      ] = tcount 
    summary['Pass rate'  ] = prate 

    # if result.wasSuccessful():    # relegate this to print_summary()
    print_summary(summary)

    return summary, result




# ------------------------------------------------------------ #
def append_summary(master, summary):
    if not master:
        master = summary.copy() 
        master['Name'] = 'ALL TESTS'
        master['Sublist'] = [summary.copy()]     # store list of all test summaries
        return master 

    for k in master.keys(): 
        if k == 'Sublist': 
            master['Sublist'].append(summary.copy())
        else:
            master[k] += summary[k] 

    if not master.has_key('Sublist'):
        master['Sublist'] = [summary.copy()]     # store list of all test summaries

    master['Pass rate'] = round( 100.0* master['Pass']/float(master['Total']), 2)
    master['Name'] = 'ALL TESTS'

    return master


# ------------------------------------------------------------ #
def print_breakdown(slist):
    """Prints breakdown of other tests in slist in shortened form""" 
    print '   Name', ' '*20, 'Pass/Total  Fail Error PassRate '
    for s in slist: # slist is list of dict()s 
        n = s['Name'] 
        p = s['Pass'] 
        f = s['Failures']
        e = s['Errors']
        t = s['Total'] 
        pr = str(s['Pass rate']) + '%' 

        spc = ' '*(24 - len(n))
        print '   %s %s    %03d/%03d   %03d   %03d   %s ' % (n, spc, p, t, f, e, pr) 


# ------------------------------------------------------------ #
def print_summary(summary, title=None):
    if title==None:
        title = "SUMMARY FOR '%s'" % (summary['Name'])
    print 
    print "*%s*" % (title) 
    print "-" * 60
   
    if summary.has_key('Sublist'):
        print_breakdown(summary['Sublist'])

    print "-" * 60
    print "    Name       :", summary['Name'] 
    print "    Pass       :", summary['Pass'] 
    print "    Failures   :", summary['Failures']
    print "    Errors     :", summary['Errors']
    print "    Total count:", summary['Total'] 
    print "    Pass rate  :", str(summary['Pass rate']) + '%' 
    print "-" * 60

    print
    s = summary
    if summary['Pass'] == summary['Total']: 
        print "All tests ran without problems :)"
    else:
        print s['Pass'], "out of", s['Total'], "tests ran without problems. There were", s['Errors']+s['Failures'], "fails or errors"
    print
    print "=" * 60




# ------------------------------------------------------------ #
def dbexec_cmd(cmdstr, dbfile):
    results = [] 
    try:
        con = sqlite3.connect(dbfile)
        cur = con.cursor()  
        raw_data = cur.execute(cmdstr) 
        con.commit()
        for r in raw_data: results.append(r) 
        cur.close()
        con.close()
    except:
        print "ERROR. Could not execute command %s on sqlite db %s " % (cmdstr, dbfile), "for some reasone!"
        return []
    return results


# ------------------------------------------------------------ #
def dbexec_scr(scr, dbfile):
    results = [] 
    try:
        con = sqlite3.connect(dbfile)
        cur = con.cursor()  
        raw_data = cur.executescript(scr) 
        con.commit()
        for r in raw_data: results.append(r) 
        cur.close()
        con.close()
    except:
        print "ERROR. Could not execute command %s on sqlite db %s " % (scr, dbfile), "for some reasone!"
        return []
    return results



# ********************************************************************
# TODO. Considering moving the next few db funcs to different location 
# ------------------------------------------------------------ #
def dbpopulate_testoptions(dbfile):
    """Helper function to populate a sqlite database for testing instead of standard one"""
    try:
        con = sqlite3.connect(dbfile)    
        cur = con.cursor()  
        #HEADER: Strike, Symbol, Last, Chg, Bid, Ask, Vol, Open_Int, Exp, Ticker, Otype 
        #ORDER:       0,      1,    2,   3,   4,   5,   6,        7,   8,      9,    10 
        cur.executescript("""
        DROP TABLE IF EXISTS OptionsTable;
        CREATE TABLE IF NOT EXISTS OptionsTable (Strike REAL, Symbol TEXT PRIMARY KEY, Last REAL, Chg REAL, Bid REAL, 
            Ask REAL, Vol INT, Open_Int INT, Exp TEXT, Ticker TEXT, Otype CHARACTER(1));
        INSERT INTO OptionsTable VALUES(45.0,'FB140322C00045000',19.1,'N/A',19.35,19.6,21,6647,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(46.0,'FB140322C00046000',18.25,'N/A',18.25,18.65,3,2826,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(47.0,'FB140322C00047000',17.5,'N/A',17.4,17.6,72,6251,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(48.0,'FB140322C00048000',16.25,'N/A',16.35,16.6,2080,9791,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(49.0,'FB140322C00049000',15.48,'N/A',15.4,15.65,50,6849,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(50.0,'FB140322C00050000',14.5,'N/A',14.4,14.6,396,24434,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(52.5,'FB140322C00052500',12.2,'N/A',12.05,12.2,215,10031,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(55.0,'FB140322C00055000',9.85,'N/A',9.75,9.9,1361,22555,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(57.5,'FB140322C00057500',7.7,'N/A',7.6,7.85,3411,18994,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(60.0,'FB140322C00060000',5.85,'N/A',5.8,5.9,4349,37181,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(62.5,'FB140322C00062500',4.25,'N/A',4.2,4.3,3549,14466,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(65.0,'FB140322C00065000',3.0,'N/A',2.99,3.0,10333,39513,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(67.5,'FB140322C00067500',2.06,'N/A',2.04,2.06,3616,15925,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(70.0,'FB140322C00070000',1.4,'N/A',1.38,1.39,3597,21814,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(75.0,'FB140322C00075000',0.65,'N/A',0.63,0.65,1732,17105,'2014-03-22','FB','C');
        INSERT INTO OptionsTable VALUES(45.0,'FB140322P00045000',0.05,'N/A',0.02,0.07,352,13925,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(46.0,'FB140322P00046000',0.06,'N/A',0.05,0.06,8,4714,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(47.0,'FB140322P00047000',0.07,'N/A',0.05,0.08,78,14172,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(48.0,'FB140322P00048000',0.1,'N/A',0.07,0.1,22,5926,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(49.0,'FB140322P00049000',0.1,'N/A',0.08,0.1,123,2789,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(50.0,'FB140322P00050000',0.12,'N/A',0.11,0.12,131,9177,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(52.5,'FB140322P00052500',0.22,'N/A',0.21,0.22,923,14055,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(55.0,'FB140322P00055000',0.41,'N/A',0.4,0.42,813,10750,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(57.5,'FB140322P00057500',0.78,'N/A',0.77,0.78,6196,22153,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(60.0,'FB140322P00060000',1.39,'N/A',1.39,1.4,6410,9484,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(62.5,'FB140322P00062500',2.32,'N/A',2.31,2.32,6416,4385,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(65.0,'FB140322P00065000',3.55,'N/A',3.55,3.6,5880,2315,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(67.5,'FB140322P00067500',5.1,'N/A',5.1,5.15,3518,612,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(70.0,'FB140322P00070000',6.9,'N/A',6.9,7.0,142,452,'2014-03-22','FB','P');
        INSERT INTO OptionsTable VALUES(75.0,'FB140322P00075000',12.85,'N/A',11.05,11.4,6,248,'20140322','FB','P');
        INSERT INTO OptionsTable VALUES(59.0,'FB140307C00059000',4.65,'N/A',5.95,6.3,67,74,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(60.0,'FB140307C00060000',5.3,'N/A',5.3,5.45,13,147,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(61.0,'FB140307C00061000',4.55,'N/A',4.6,4.75,18,175,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(62.0,'FB140307C00062000',4.0,'N/A',3.95,4.05,148,231,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(63.0,'FB140307C00063000',3.3,'N/A',3.35,3.45,112,1211,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(65.0,'FB140307C00065000',2.45,'N/A',2.39,2.42,75,698,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(70.0,'FB140307C00070000',0.92,'N/A',0.94,0.97,332,2079,'2014-03-07','FB','C');
        INSERT INTO OptionsTable VALUES(50.0,'FB140307P00050000',0.15,'N/A',0.05,0.11,1,182,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(52.0,'FB140307P00052000',0.37,'N/A',0.09,0.14,9,9,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(55.0,'FB140307P00055000',0.23,'N/A',0.21,0.24,9,119,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(56.0,'FB140307P00056000',0.57,'N/A',0.3,0.31,20,97,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(59.0,'FB140307P00059000',0.89,'N/A',0.7,0.74,247,364,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(60.0,'FB140307P00060000',0.94,'N/A',0.93,0.96,72,203,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(61.0,'FB140307P00061000',2.18,'N/A',1.2,1.24,26,377,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(62.0,'FB140307P00062000',1.73,'N/A',1.54,1.58,42,329,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(63.0,'FB140307P00063000',1.95,'N/A',1.94,1.98,136,201,'2014-03-07','FB','P');
        INSERT INTO OptionsTable VALUES(65.0,'FB140307P00065000',2.95,'N/A',2.94,2.99,70,8,'2014-03-07','FB','P');
        """)
        con.commit()
        cur.close()
        con.close()
    except:
        print "ERROR. Could not populate test cache db", dbfile, "for some reasone!"




