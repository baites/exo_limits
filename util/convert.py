#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

from __future__ import print_function

import os
import yaml

def convert(input_yaml, output_yaml, overwrite=False, verbose=False):
    '''Convert error band absolute values to deviations

    The input yaml format is set of lines:

        X: [expected, y_sigma_down, y_sigma_up,
                      y_2sigma_down, y_2sigma_up, observed]

    where y values are absolute. The script will generate on output yaml
    file with lines:

        X: [expected, sigma_up, sigma_down, 2sigma_up, 2sigma_down, observed]

    where all values are relative except X, expected and observed. Note swap of
    sigma UP and DOWN values in output compared to input

    EXAMPLE

        input:

            10: [50, 40, 60, 30, 70, 55]
            15: [45, 40, 50, 35, 55, 44]

        output:

            10: [50, 10, -10, 20, -20, 55]
            15: [45, 5, -5, 10, -10, 44]
    '''

    if not os.path.exists(input_yaml):
        raise RuntimeError("input file does not exist: " + input_yaml)

    if os.path.exists(output_yaml) and not overwrite:
        raise RuntimeError(("output file exists: use -f (--force) flag to "
                            "force overwrite"))

    if verbose:
        print("- read yaml input", end=' ... ')

    # read input YAML
    data = None
    with open(input_yaml, 'r') as input_:
        data = yaml.load('\n'.join(input_.readlines()))

    if not data:
        raise RuntimeError("failed to read input yaml")

    if verbose:
        print("done")

    if verbose:
        print("- convert yaml error band absolute values to deviations",
              end=' ... ')

    # convert YAML
    data = {k: [v[0], # expected
                v[2] - v[0], v[1] - v[0], # 1-sigma band
                v[4] - v[0], v[3] - v[0], # 2-sigma band
                v[5] # observed
               ] for k, v in data.items()}

    if verbose:
        print("done")

    if verbose:
        print("- save data in output file", end=' ... ')

    # save YAML
    saved = False
    with open(output_yaml, 'w') as output_:
        yaml.dump(data, output_)
        saved = True

    if not saved:
        raise RuntimeError("failed to save yaml")

    if verbose:
        print("done")
