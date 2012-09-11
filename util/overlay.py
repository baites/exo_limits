#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 11, 2012
Copyright 2012, All rights reserved
'''

from __future__ import print_function,division

import copy
import math
from optparse import OptionParser

from array import array
import ROOT

from loader import load_data,get_limits
import labels
import style
import theory
import smooth 
from exclusion import exclude

def gev_to_tev(values):
    '''Convert GeV axis to TeV: divide by 1000'''

    return [x * 1e-3 for x in values]

def plot(limit_type, low_mass, high_mass, logy=True, smooth_data=True):
    '''
    Application entry point
    '''

    supported_limit_types = ("narrow", "wide", "kk")
    if limit_type not in supported_limit_types:
        raise RuntimeError("supported limit types: {0!r}".format(
                            supported_limit_types))

    data = load_data(low=low_mass, high=high_mass)

    class Limits(object): pass

    # container for low and high limits
    limits = Limits
    limits.low = {
            "visible": None,
            "invisible": None
            }

    limits.high = copy.deepcopy(limits.low)
    limits.low_fix_observed = copy.deepcopy(limits.low)

    # convert YAML to dictionary
    split_point = {
            "narrow": 1000,
            "wide": 1100,
            "kk": 1000
            }.get(limit_type)

    (limits.low["visible"],
     limits.low["invisible"]) = get_limits(data.low, is_low_mass=True,
                                           split_point=split_point,
                                           transform_x=gev_to_tev)

    (limits.high["visible"],
     limits.high["invisible"]) = get_limits(data.high, is_low_mass=False,
                                            split_point=split_point,
                                            transform_x=gev_to_tev)

    (limits.low_fix_observed["visible"],
     limits.low_fix_observed["invisible"]) = get_limits(data.low, is_low_mass=True,
                                                        split_point=split_point,
                                                        low_mass_x=True,
                                                        transform_x=gev_to_tev)

    if smooth_data:
        smooth.data(limits.high["visible"], n=2)

    legend = ROOT.TLegend(0.5, 0.50, 0.80, 0.88)

    line_width = 3
    combo = ROOT.TMultiGraph()

    # 2 sigma band
    cur = limits.low["visible"]
    graph = ROOT.TGraphAsymmErrors(len(cur["x"]), cur["x"], cur["expected"],
                                   cur["xerr"], cur["xerr"],
                                   cur["two_sigma_down"], cur["two_sigma_up"])
    graph.SetFillColor(ROOT.kGray + 1)
    graph.SetLineWidth(0)
    combo.Add(graph)
    g_2s_lm = graph

    cur = limits.high["visible"]
    graph = ROOT.TGraphAsymmErrors(len(cur["x"]), cur["x"], cur["expected"],
                                   cur["xerr"], cur["xerr"],
                                   cur["two_sigma_down"], cur["two_sigma_up"])
    graph.SetFillColor(ROOT.kGray + 1)
    graph.SetLineWidth(0)
    combo.Add(graph)
    g_2s_hm = graph

    # 1 sigma band
    cur = limits.low["visible"]
    graph = ROOT.TGraphAsymmErrors(len(cur["x"]), cur["x"], cur["expected"],
                                   cur["xerr"], cur["xerr"],
                                   cur["one_sigma_down"], cur["one_sigma_up"])
    graph.SetFillColor(ROOT.kGray)
    graph.SetLineWidth(0)
    combo.Add(graph)
    g_1s_lm = graph

    cur = limits.high["visible"]
    graph = ROOT.TGraphAsymmErrors(len(cur["x"]), cur["x"], cur["expected"],
                                   cur["xerr"], cur["xerr"],
                                   cur["one_sigma_down"], cur["one_sigma_up"])
    graph.SetFillColor(ROOT.kGray)
    graph.SetLineWidth(0)
    combo.Add(graph)
    g_1s_hm = graph

    # expected
    cur = limits.low["visible"]
    graph = ROOT.TGraph(len(cur["x"]), cur["x"], cur["expected"])
    graph.SetLineColor(ROOT.kBlack)
    graph.SetLineWidth(line_width)
    combo.Add(graph)
    legend.AddEntry(graph, "Expected (95% CL)", "l")

    cur = limits.high["visible"]
    graph = ROOT.TGraph(len(cur["x"]), cur["x"], cur["expected"])
    graph.SetLineColor(ROOT.kBlack)
    graph.SetLineWidth(line_width)
    combo.Add(graph)

    # observed
    cur = limits.low_fix_observed["visible"]
    graph = ROOT.TGraph(len(cur["observed_x"]), cur["observed_x"], cur["observed"])
    graph.SetLineColor(ROOT.kRed + 1)
    graph.SetLineWidth(line_width)
    graph.SetLineStyle(2)
    combo.Add(graph)
    legend.AddEntry(graph, "Observed (95% CL)", "l")

    cur = limits.high["visible"]
    graph = ROOT.TGraph(len(cur["observed_x"]), cur["observed_x"], cur["observed"])
    graph.SetLineColor(ROOT.kRed + 1)
    graph.SetLineWidth(line_width)
    graph.SetLineStyle(2)
    combo.Add(graph)

    # Theory
    theories = {
            "narrow": ([theory.zprime, 1.2, False], ),
            "wide": ([theory.zprime, 10.0, False], ),
            "kk": ([theory.kkgluon, None, None], )
            }.get(limit_type)

    for index, (theory_function, theory_width, use_old_theory) in enumerate(theories, 0):
        class Theory(object): pass

        x, y, label = (theory_function(theory_width, use_old_theory)
                        if theory_width
                        else theory_function())

        # remove all the points below 500 GeV
        x, y = zip(*[(xi, yi) for xi, yi in zip(x, y) if not 500 > xi])

        x = gev_to_tev(x)
        graph = ROOT.TGraph(len(x), array('d', x), array('d', y))
        graph.SetLineColor([ROOT.kBlue + 1, ROOT.kMagenta + 1, ROOT.kGreen + 1][index] if index < 3 else ROOT.kBlue + 1)
        graph.SetLineWidth(3)
        graph.SetLineStyle(9)
        combo.Add(graph)
        legend.AddEntry(graph, label, "l")

        theory_data = Theory()
        theory_data.x = x
        theory_data.y = y

        '''
        print("low mass".capitalize())
        expected_exclusion, observed_exclusion = exclude(limits.low["visible"], theory_data)

        print("Expected exclusion:", expected_exclusion)
        print("Observed exclusion:", observed_exclusion)

        print()
        print("high mass".capitalize())
        expected_exclusion, observed_exclusion = exclude(limits.high["visible"], theory_data)

        print("Expected exclusion:", expected_exclusion)
        print("Observed exclusion:", observed_exclusion)
        '''

    legend.AddEntry(g_1s_lm, "Expected #pm 1 s.d.", "f")
    legend.AddEntry(g_2s_lm, "Expected #pm 2 s.d.", "f")

    # Draw
    cv = ROOT.TCanvas()
    style.canvas(cv)

    combo.Draw("3al")

    # Split point
    if limit_type != 'kk':
        line = ROOT.TGraph(2)
        line.SetPoint(0, split_point * 1e-3, 1e1)
        line.SetPoint(1, split_point * 1e-3, 3e-2)
        line.SetLineColor(ROOT.kGray + 2)
        line.SetLineStyle(9)
        line.SetLineWidth(3)
        line.Draw("L")

    legend.Draw()

    if logy:
        cv.SetLogy(True)

    if limit_type == 'kk':
        style.combo(combo, maximum=1e2 if logy else None, ytitle="Upper Limit #sigma_{KK} x B [pb]")
    else:
        style.combo(combo, maximum=1e2 if logy else None)

    style.legend(legend)
    legend.SetTextSize(0.04)

    plot_labels = labels.create({
        #"narrow": "{0:.1f}% Width Assumption".format(theory_width if theory_width else 0),
        "narrow": "Z' with 1.2% Decay Width",
 
        "wide": "Z' with 10% Decay Width",
        "kk": "KK Gluon"}.get(limit_type, None))
    map(ROOT.TObject.Draw, plot_labels)

    cv.Update()
    cv.SaveAs("limits-{0}.pdf".format(limit_type))
