#!/usr/bin/env python2.7
# Exectute this file with -v @ the end. Cannot use ipython

from __future__ import print_function

# -- Standard boilerplate header - begin
import unittest as ut
import sys, os
from os.path import abspath, dirname

cdir = dirname(abspath(sys.argv[0]))        # current dir (testdir)
pdir = dirname(cdir)                        # parent dir
sys.path.insert(0, os.path.join(pdir, 'mhut'))

pathlist = []
for p in sys.path:
    if not p in pathlist: pathlist.append(p)
sys.path = pathlist
# for p in sys.path: print '  -> ', p

from testutils import run_tests
# -- Standard boilerplate header - end


from timeutils import format_date, parse_date , iso_date
import datetime as dt

'''Tests timeutils class'''


class TestTimeutils(ut.TestCase):
    def setUp(self):
        self.date_obj = dt.date(2013, 5, 24)  # date_obj is a datetime.date object
        self.datestr = "2013-05-24"

    def tearDown(self):
        pass


    def test_format_date(self):
        """Have day, month, year"""
        self.assertEqual(format_date(self.date_obj), self.datestr)


    def test_format_date1(self):
        """Have only month and year"""
        date_obj = dt.date(2013, 5, 1)  # date_obj is a datetime.date object
        self.assertEqual(format_date(date_obj), "2013-05")


    def test_parse_date(self):
        """Have day, month and year"""
        self.assertEqual(parse_date('may24.13').isoformat(), self.datestr)
        self.assertEqual(parse_date('20140918').isoformat(), "2014-09-18")
        self.assertEqual(parse_date('2014-09-18').isoformat(), "2014-09-18")
        self.assertEqual(parse_date('jul9.2014').isoformat(), "2014-07-09")
        self.assertEqual(parse_date('jul09.14').isoformat(), "2014-07-09")

        self.assertEqual(parse_date('jul23.14').isoformat(), '2014-07-23')
        self.assertEqual(parse_date('20140918').isoformat(), '2014-09-18')
        self.assertEqual(parse_date('2014-09-18').isoformat(), '2014-09-18')
        self.assertEqual(parse_date('2014.9').isoformat(), '2014-09-01')
        self.assertEqual(parse_date('jul9.2014').isoformat(), '2014-07-09')
        self.assertEqual(parse_date('jul09.14').isoformat(), '2014-07-09')
        self.assertEqual(parse_date('july-2014').isoformat(), '2014-07-01')
        self.assertEqual(parse_date('july-14').isoformat(), '2014-07-01')

        self.assertEqual(parse_date('9/7/14').isoformat(), '2014-09-07')
        self.assertEqual(parse_date('9/7/2014').isoformat(), '2014-09-07')
        self.assertEqual(parse_date('09/7/14').isoformat(), '2014-09-07')
        self.assertEqual(parse_date('9/07/14').isoformat(), '2014-09-07')
        self.assertEqual(parse_date('09/07/14').isoformat(), '2014-09-07')
        self.assertEqual(parse_date('09/07/2014').isoformat(), '2014-09-07')

    def test_parse_date2(self):
        """Have only month and year"""
        self.assertEqual(parse_date('2014.9').isoformat(), "2014-09-01")
        self.assertEqual(parse_date('july-2014').isoformat(), "2014-07-01")
        self.assertEqual(parse_date('july-14').isoformat(), "2014-07-01")



    def test_parse_date3(self):
        """Bad options that are expected to fail"""
        self.assertNotEqual(parse_date('8.18.2014').isoformat(),    "2014-08-18")
        self.assertNotEqual(parse_date('2012091').isoformat(),      "2012-09-01")
        self.assertNotEqual(parse_date('113-13-59').isoformat(),    "2013-13-59")
        self.assertNotEqual(parse_date('01131359').isoformat(),     "2013-13-59")
        self.assertNotEqual(parse_date('jux.14').isoformat(),       "2014-xx-14")

    def test_iso_date(self):
        self.assertTrue (iso_date('2013-05-07'))
        self.assertTrue (iso_date('2013-99-77')) # crazy but isoformat
        self.assertFalse(iso_date( 20130917   )) # not a string
        self.assertFalse(iso_date('13-09-17'  )) # < 8 chars
        self.assertFalse(iso_date('2013-09-179'))# > 8 chars
        self.assertFalse(iso_date('2013--0917')) # less than 3-tuple
        self.assertFalse(iso_date('20-13-09-7')) # more than 3-tuple

if __name__ == '__main__':
    #ut.main()   # standard way to call tests
    run_tests(TestTimeutils)
