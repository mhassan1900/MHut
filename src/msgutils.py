#!/usr/bin/env python2.7

'''
Message utils for printing. Replacing w/logging later on
'''

_MAXCHAR_ = 24
_EPS_ = 0.0000001
_MAXPRICE = 1000        # use reset and rescale to force max prices
_SCALE = 2.1            # default scaling factor from max breakeven price 
_USE_MIDPOINT_ = True # False

#NOTE. Use self.add_stock.__doc__ for direct help instead of separate string


############################################################
######################## MESSAGES ########################## 
############################################################
def wmsg(*msg):
    """Warning message.""" 
    if len(msg) == 0: print "WARNING! Could not perform requestion action"
    else:
        print "WARNING:", 
        for m in msg: print m,
        print

def dmsg(*msg):
    """Warning message.""" 
    if len(msg) == 0: print "DEBUG!=> [Default notifier]"
    else:
        print "DEBUG:=>", 
        for m in msg: print m,
        print

def emsg(*msg):
    """Error message. Prints but does not exit"""
    if len(msg) == 0: print "ERROR! Could not perform requestion action"
    else:
        print "ERROR",
        for m in msg: print m,
        print


def fatal_error(*msg):
    """Fatal error message. Prints and exits"""
    if len(msg) == 0: print "FATAL ERROR! Exiting."
    else:
        for m in msg: print m,
        print
    exit(1)



############################################################
#################### PRETTY PRINTING ####################### 
############################################################
def delimit(msg=None):
    if msg == None:
        print '\n', '-' * 40, '\n'
    else:
        print '-' * 40, '\n', msg, '\n', '-' * 40

  

if __name__ == '__main__':
    pass    # for now

