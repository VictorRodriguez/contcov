#!/usr/bin/env python3

import sys
try:
    import numpy
    import scipy as cp
    from numpy import poly1d
except ImportError:
    print("ERROR %s TEST FAIL" % (sys.argv[0]))
