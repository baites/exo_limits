#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

import copy
import math
import os
import yaml

from array import array

def load_file(filename):
    '''
    Load yaml data from file
    
    raise RuntimeError in case of error: file does not exist or load failed
    '''

    if not os.path.exists(filename):
        raise RuntimeError("input file does not exist: " + filename)

    data = None
    with open(filename) as input_:
        data = yaml.load('\n'.join(input_.readlines()))

    if not data:
        raise RuntimeError("failed to read input data from " + filename)

    return data

def load_data(**kargs):
    '''
    Load several YAML files and put into Data object

    The Data attributes are defined by argument names, e.g.:

        data = load_data(low="low_file.yaml", high="high_file.yaml")
        print(data.low)
        print(data.high)
    '''

    # Dummy container for attribute reference instead of indexing
    class Data(object): pass

    data = Data()

    # Load each and every file specified in argument(s)
    for k, v in kargs.items():
        data.__dict__[k] = load_file(v)

    return data

def get_limits(data, is_low_mass=True, split_point=1000, low_mass_x=False,
               transform_x=None):
    '''Convert yaml data into Dictionary like format'''

    visible = {
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

    invisible = copy.deepcopy(visible)

    def fill(data, mass, to_, x=None):
        v = data[mass]
        to_["x"].append(x if x else mass)
        to_["xerr"].append(0)
        to_["expected"].append(v[0])
        to_["one_sigma_up"].append(v[1])
        to_["one_sigma_down"].append(math.fabs(v[2]))
        to_["two_sigma_up"].append(v[3])
        to_["two_sigma_down"].append(math.fabs(v[4]))
        to_["observed"].append(v[5])
        to_["observed_x"].append(x if x else mass)

    for k in sorted(data):
        if k == split_point:
            if k in data:
                if low_mass_x and is_low_mass:
                    fill(data, k, visible, x=k - 10)
                    fill(data, k, invisible, x=k - 10)
                else:
                    fill(data, k, visible)
                    fill(data, k, invisible)

            continue

        if is_low_mass:
            if k < split_point:
                cur = visible
            else:
                cur = invisible
        else:
            if k > split_point:
                cur = visible
            else:
                cur = invisible

        fill(data, k, cur)

    if transform_x:
        visible['x'] = array('d', transform_x(visible['x']))
        visible['observed_x'] = array('d', transform_x(visible['observed_x']))

        invisible['x'] = array('d', transform_x(invisible['x']))
        invisible['observed_x'] = array('d', transform_x(invisible['observed_x']))

    return visible, invisible
