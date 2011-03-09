#!/usr/bin/env python
import sys
import scipy
import pylab
from analyze_trial import get_period

GRAV_CONST = 9.81

data_files = sys.argv[1:]

period_vals = []
length_vals = []

# Read data file and compute periods
for file_name in data_files:
    print 'analyzing: ', file_name
    pend_len, period = get_period(file_name) 
    print '  length: ', pend_len
    print '  period: ', period
    period_vals.append(period)
    length_vals.append(pend_len)

period_vals = scipy.array(period_vals)
length_vals = scipy.array(length_vals)

length_max = length_vals.max()
length_min = length_vals.min()

length_model = scipy.linspace(length_min, length_max, 100)
period_model = 2.0*scipy.pi*scipy.sqrt(length_model/GRAV_CONST)

pylab.plot(length_model, period_model, 'b')
pylab.plot(length_vals, period_vals, 'or')
pylab.xlabel('length (m)')
pylab.ylabel('period (s)')
pylab.grid('on')
pylab.show()






