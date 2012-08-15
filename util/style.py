#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

import ROOT

def canvas(cv):
    '''Set canvas margins for pretty plot

    The canvas is expected to contain only one Pad.
    '''

    pad = cv.cd(1)
    pad.SetTopMargin(0.1)
    pad.SetRightMargin(0.03)
    pad.SetBottomMargin(0.15)
    pad.SetLeftMargin(0.15)

def combo(obj, xtitle="M_{t#bar{t}} [TeV]",
          ytitle="Upper Limit #sigma_{Z'} x B [pb]", maximum=1e1):
    '''Adjust TMultiGraph style'''

    obj.SetMinimum(3e-2)

    if maximum:
        obj.SetMaximum(maximum)

    obj.GetXaxis().SetTitle(xtitle)
    obj.GetYaxis().SetTitle(ytitle)

    for axis in obj.GetXaxis(), obj.GetYaxis():
        axis.SetTitleFont(62)
        axis.SetTitleOffset(1.0)
        axis.SetTitleSize(0.06)
        axis.SetLabelFont(42)
        axis.SetLabelSize(0.05)

def legend(obj):
    '''Remove border and set white background in TLegend'''

    obj.SetFillColor(ROOT.kWhite)
    obj.SetBorderSize(0)
    obj.SetTextFont(42)
    obj.SetTextSize(0.06)
