#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 11, 2012
Copyright 2012, All rights reserved
'''

from __future__ import division

from array import array
import numpy, math
from scipy import interpolate

def smooth(x, y, new_x=None, log=False, order=2, relunc=0.05):
    '''Smooth y points with B-spline method (see SciPy for details)

    The function consists for two steps:

        - get smooth function
        - evaluate function at each X value to get new Y

    the new set of y values is returned.

    note: new Y's can be evaluated at new set of X's if passed with new_x
    '''

    # do nothing if there is insufficient number of points passed
    if 2 > len(x): return y

    if log: y = [math.log(yi) for yi in y]

    tck = interpolate.splrep(x, y, w=[1.0/(relunc * yi) for yi in y], k=order) 

    if log:
        return [math.exp(yi) for yi in interpolate.splev(new_x, tck)]
    return interpolate.splev(new_x, tck)


def data(data, n=3, log=False):
    '''
    Smooth data error bands and expected curve

    The function will update data with smothened curve evaluated at new,
    evenly spaced values of X

    arguments:
        data: dictionary of expected values, error bands and X's
        n: used in increasing number of X evenly spaced points:
           len(x) -> n * len(x)
    '''

    '''Convert yaml data into Dictionary like format'''

    limits = {
            "x": array('d'),
            "xerr": array('d'),
            "expected": array('d'),
            "observed": array('d'),
            "observed_x": array('d'),
            "one_sigma_down": array('d'),
            "one_sigma_up": array('d'),
            "two_sigma_down": array('d'),
            "two_sigma_up": array('d')
            }

    for mass in sorted(data):
        v = data[mass]
        limits["x"].append(mass)
        limits["xerr"].append(0)
        limits["expected"].append(v[0])
        limits["one_sigma_up"].append(v[1])
        limits["one_sigma_down"].append(math.fabs(v[2]))
        limits["two_sigma_up"].append(v[3])
        limits["two_sigma_down"].append(math.fabs(v[4]))
        limits["observed"].append(v[5])
        limits["observed_x"].append(mass)

    x = limits['x']
    if 2 > len(x): return

    # Get new set X's that are evenly spaced in the range [x_min, x_max]
    new_x = list(numpy.linspace(x[0], x[-1], n * len(x)))
    new_x.extend([e for e in x if not e in new_x])
    new_x.sort()

    # Cache new expected values as the old ones are still neeeded
    new_expected = smooth(x, limits["expected"], new_x=new_x, relunc=0.01)

    # Smooth also the observed results
    new_observed = smooth(x, limits["observed"], new_x=new_x, log=log, order=1, relunc=0.01)

    # Smooth error bands: need to work with absolute values of Y instead of
    # sigma's
    for key in ("one_sigma_up",
                "two_sigma_up"):

        # Get absolute values
        y = [yi + sigmai for yi, sigmai in zip(limits['expected'], limits[key])]

        # Smooth these
        y = smooth(x, y, new_x=new_x)
        limits[key] = array('d', [yh - yi for yi, yh in zip(new_expected, y)])

    # Do the same for sigma down
    for key in ("one_sigma_down",
                "two_sigma_down"):

        # Get abosolute values
        y = [yi - sigmai for yi, sigmai in zip(limits['expected'], limits[key])]

        # Smooth y values
        y = smooth(x, y, new_x=new_x)
        limits[key] = array('d', [yi - yl for yi, yl in zip(new_expected, y)])

    # Update expected values
    limits["expected"] = array('d', new_expected)
    limits["observed"] = array('d', new_observed)

    # Update x-values
    limits['x'] = array('d', new_x)
    limits['xerr'] = array('d', (0 for x in new_x))
    limits['observed_x'] = array('d', new_x)

    data.clear()
    index = 0

    for mass in limits['x']:
        data[mass] = array('d')
        data[mass].append(limits['expected'][index])
        data[mass].append(limits['one_sigma_up'][index])
        data[mass].append(limits['one_sigma_down'][index])
        data[mass].append(limits['two_sigma_up'][index])
        data[mass].append(limits['two_sigma_down'][index])
        data[mass].append(limits['observed'][index])
        index = index + 1

