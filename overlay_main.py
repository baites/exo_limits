#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 07, 2012
Copyright 2012, All rights reserved
'''

from __future__ import print_function,division

from optparse import OptionParser
import sys

def parser():
    parser = OptionParser(usage=("usage: %prog [options] low_mass.yaml "
                                 "high_mass.yaml"))

    parser.add_option("-b", "--batch",
                      action="store_true", default=False,
                      help="Run application in batch mode")

    parser.add_option("--type",
                      action="store", default=None, dest="type_",
                      help="input type: kk|narrow|wide")

    parser.add_option("--no-log",
                      action="store_true", default=False,
                      help="Use normal y-scale")

    parser.add_option("-v", "--verbose",
                      action="store_true", default=False,
                      help="verbose yaml convertion")

    parser.add_option("--smooth",
                      action="store_true", default=False,
                      help="Turn-on smoothing")

    return parser

def main():
    class HelpExit(Exception): pass

    verbose = False

    option_parser = None
    try:
        option_parser = parser()
        options, args = option_parser.parse_args()

        verbose = options.verbose

        if not args:
            raise HelpExit()

        if 2 != len(args):
            raise RuntimeError("only two posiitonal arguments are accepted")

        if not options.type_:
            raise RuntimeError("input type is not supplied")

        # import templates only here otherwise PyROOT inhercepts --help option
        from util.overlay import plot

        plot(options.type_.lower(), *args, logy=not options.no_log,
             smooth_data=options.smooth)
    except HelpExit:
        option_parser.print_help()

        return 1

    except Exception as error:
        if verbose:
            # print Exception traceback for debug
            import traceback

            traceback.print_tb(sys.exc_info()[2])

        print(error, file=sys.stderr)

        return 1
    else:
        return 0

if __name__ == "__main__":
    sys.exit(main())
