#!/usr/bin/env python

'''
5reated by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

import ROOT

def create(title=None):
    '''Create ROOT labels to be shown on all plots

    Two labels will be returned: CMS experiment with luminosity and sub-title.
    '''

    experiment = ROOT.TLatex(0.15, 0.92,
                             "CMS, L = 19.6 fb^{-1}, #sqrt{s} = 8 TeV")
    experiment.SetNDC() # Use canvas coordinates
    experiment.SetTextFont(62)
    experiment.SetTextSize(0.046)

    sub_title = ROOT.TLatex(0.97, 0.92, title if title else "")
    sub_title.SetNDC() # Use canvas coordinates
    sub_title.SetTextAlign(31)
    sub_title.SetTextFont(62)
    sub_title.SetTextSize(0.046)

    return experiment, sub_title
