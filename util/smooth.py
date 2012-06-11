#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 11, 2012
Copyright 2012, All rights reserved
'''

from __future__ import division

from array import array
import numpy
from scipy import interpolate

def smooth(x, y, s=None, relunc=0.05, new_x=None):
    '''Smooth y points with B-spline method (see SciPy for details)

    The function consists for two steps:

        - get smooth function
        - evaluate function at each X value to get new Y

    the new set of y values is returned.

    note: new Y's can be evaluated at new set of X's if passed with new_x
    '''

    # do nothing if there is insufficient number of points passed
    if 2 > len(x):
        return y

    tck = interpolate.splrep(x, y,
                             w=[1 / (relunc * yi) for yi in y],
                             s=s)

    return interpolate.splev(new_x if new_x else x, tck)

def data(data, n=3):
    '''
    Smooth data error bands and expected curve

    The function will update data with smothened curve evaluated at new,
    evenly spaced values of X

    arguments:
        data: dictionary of expected values, error bands and X's
        n: used in increasing number of X evenly spaced points:
           len(x) -> n * len(x)
    '''

    if 2 > len(data['x']):
        return

    # cache x for fast access
    x = data['x']

    # Get new set X's that are evenly spaced in the range [x_min, x_max]
    new_x = tuple(numpy.linspace(x[0], x[-1], n * len(x)))

    # Cache new expected values as the old ones are still neeeded
    new_expected = smooth(x, data["expected"], s=len(x) / 2, new_x=new_x)

    # Smooth error bands: need to work with absolute values of Y instead of
    # sigma's
    for key in ("one_sigma_up",
                "two_sigma_up"):

        # Get absolute values
        y = [yi + sigmai for yi, sigmai in zip(data['expected'], data[key])]

        # Smooth these
        y = smooth(x, y, s=len(x) / 2, new_x=new_x)
        data[key] = array('d', [yh - yi for yi, yh in zip(new_expected, y)])

    # Do the same for sigma down
    for key in ("one_sigma_down",
                "two_sigma_down"):

        # Get abosolute values
        y = [yi - sigmai for yi, sigmai in zip(data['expected'], data[key])]

        # Smooth y values
        y = smooth(x, y, s=len(x) / 2, new_x=new_x)
        data[key] = array('d', [yi - yl for yi, yl in zip(new_expected, y)])

    # Update expected values
    data["expected"] = array('d', new_expected)

    # Update x-values
    data['x'] = array('d', new_x)
    data['xerr'] = array('d', (0 for x in new_x))
