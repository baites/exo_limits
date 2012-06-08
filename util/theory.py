#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

def zprime(width, use_old=False):
    '''
    Zprime theoretical cross-sections

    supported mass widths are:

        1.0, 1.2, 2.0, 10.0

    a RuntimeError exception is raised if unsupported width is used

    source: http://arxiv.org/pdf/1112.4928v2.pdf, table II
    LO is scaled to NLO by 1.3 k-factor

    return: x, y, label
    '''

    def old(width, kfactor=1.3):
        x = range(700, 2001, 100)
        y = (0.3744E+01, 0.2128E+01, 0.1265E+01, 0.7784E+00, 0.4919E+00,
             0.3174E+00, 0.2081E+00, 0.1382E+00, 0.9276E-01, 0.6275E-01,
             0.4272E-01, 0.2923E-01, 0.2008E-01, 0.1383E-01)

        return x, [yi * kfactor * width for yi in y]

    # cross sections form the reference. key - Z' mass width (in %), values
    # are x-section(s)
    xsections = {
            1.0: (24.82, 12.17, 6.76, 3.66, 2.74, 2.05, 1.20, 0.753, 0.236,
                  8.20E-02, 3.71E-02, 1.16E-02, 1.90E-03, 3.59E-04),
            1.2: (29.61, 14.61, 8.07, 4.39, 3.28, 2.47, 1.44, 0.905, 0.283,
                  9.87E-02, 4.48E-02, 1.41E-02, 2.36E-03, 4.64E-04),
            2.0: (48.24, 24.37, 13.27, 7.29, 5.45, 4.13, 2.43, 1.51, 0.477,
                  0.167, 7.67E-02, 2.48E-02, 4.42E-03, 9.95E-04),
            10.0: (220.92, 115.29, 60.37, 33.07, 24.95, 19.00, 11.27, 6.91,
                   2.21, 0.777, 0.352, 0.113, 1.81E-02, 3.01E-03)
            }

    if width not in xsections:
        raise RuntimeError("only {0!r} Z' widths are supported".format(
            xsections.keys()))

    label = "Z' {0:.1f}% width, Harris et al".format(width)

    if use_old:
        x, y = old(width)
        return x, y, label

    return ((400., 500., 600., 700., 750., 800., 900.,
             1000., 1250., 1500., 1700., 2000., 2500., 3000.), 

            # Multipy x-sections by 1.3 to scale LO to NLO
            [x * 1.3 for x in xsections.get(width)],

            label)

def kkgluon():
    '''
    KK gluon theoretical cross-sections

    source: http://hep.pha.jhu.edu:8080/boostedtop/1456
    return: x, y, label
    '''

    # Note: there are 19 points: the 3000 TeV is NOT included
    return (tuple(range(1000, 3000, 100)),

            (4.5, 2.9, 1.9, 1.3, 0.9, 0.59, 0.41, 0.28, 0.21, 0.14,
             0.10, 0.07, 0.055, 0.045, 0.04, 0.031, 0.025, 0.02, 0.018, 0.014),

            "KK Gluon, Agashe et al")
