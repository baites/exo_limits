#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

from __future__ import division,print_function

import math

from scipy import interpolate

class Exclusion(object):
    def __init__(self):
        self._is_last_point_excluded = False
        self._excluded = []
        self._cache = []

    def append(self, x, is_excluded):
        if is_excluded:
            if self._is_last_point_excluded:
                pass
            else:
                self._is_last_point_excluded = True
                self._cache = []

            self._cache.append(x)
        else:
            if self._is_last_point_excluded:
                self._is_last_point_excluded = False
                self._excluded.append(self._cache)
                self._cache = []
            else:
                pass

    @property
    def excluded(self):
        return self._excluded

    def __str__(self):
        if self._cache:
            self._excluded.append(self._cache)
            self._cache = []

        return ','.join([("[{0:.2f}-{1:.2f}]".format(region[0], region[-1])
                         if 1 < len(region) else
                         "[{0}]").format(region[0]) for region in self.excluded])

def exclude(data, theory, log_scale=True):
    # interpolate theory
    ftheory = interpolate.interp1d(theory.x, map(math.log, theory.y) if log_scale else theory.y)

    # interpolate data (expected)
    fexpected = interpolate.interp1d(data["x"], map(math.log, data["expected"]) if log_scale else data["expected"])

    # interpolate data (observed)
    fobserved = interpolate.interp1d(data["observed_x"], map(math.log, data["observed"]) if log_scale else data["observed"])

    expected_exclusion = Exclusion()
    observed_exclusion = Exclusion()

    min_ = int(max(theory.x[0], data["x"][0], data["observed_x"][0]) * 1000)
    max_ = int(min(theory.x[-1], data["x"][-1], data["observed_x"][-1]) * 1000)
    print("search exclusion in x region [", min_, '-', max_, ']')

    for x in map(lambda x: x * 0.001, range(min_, max_, 1)):
        expected_exclusion.append(x, ftheory(x) > fexpected(x))
        observed_exclusion.append(x, ftheory(x) > fobserved(x))

    return expected_exclusion, observed_exclusion
