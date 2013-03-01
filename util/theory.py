#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

from __future__ import division

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
            1.0: (29.97, 14.79, 8.42, 4.78, 3.59, 2.76, 1.64, 1.03, 0.367,
                  0.133, 6.62E-02, 2.26E-02, 4.33E-03, 9.30E-04),
            1.2: (35.77, 17.82, 10.08, 5.74, 4.31, 3.32, 1.98, 1.24, 0.441,
                  0.160, 7.99E-02, 2.75E-02, 5.30E-03, 1.16E-03),
            2.0: (58.46, 29.98, 16.70, 9.57, 7.17, 5.54, 3.35, 2.08, 0.742,
                  0.273, 0.136, 4.75E-02, 9.52E-03, 2.26E-03),
            10.0: (271.98, 145.06, 77.71, 43.59, 33.29, 25.67, 15.63, 9.84,
                   3.37, 1.28, 0.616, 0.218, 4.21E-02, 8.59E-03)
            }

    if width not in xsections:
        raise RuntimeError("only {0!r} Z' widths are supported".format(
            xsections.keys()))

    label = "Z' {0:.1f}% width, Harris et al (x1.3)".format(width)

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
    KK gluon theoretical cross-sections for pp 8 TeV

    source: private comunication from Sal
    return: x, y, label
    '''
    xsections = (
        6.299, 1.81968, 0.62327, 0.24502, 0.10841, 
        0.053149, 0.028766, 0.016926 
    )

    # Note: there are 19 points: the 3000 TeV is NOT included
    return (tuple(range(1000, 3100, 300)),

            [x * 1.3 for x in xsections],

            "KK Gluon, Agashe et al (x1.3)")
