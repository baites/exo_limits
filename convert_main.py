#!/usr/bin/env python

'''
Created by Samvel Khalatyan, Jun 08, 2012
Copyright 2012, All rights reserved
'''

from __future__ import print_function

from optparse import OptionParser
import os
import sys

from util.convert import convert

def main():
    '''Run application without arguments to get help message'''

    class HelpExit(Exception): pass

    verbose = False

    try:
        # add basic arguments
        parser = OptionParser(usage=("usage: %prog input.yaml output.yaml"))
        parser.add_option("-f", "--force",
                          action="store_true", default=False,
                          help="force overwrite output file if exists")

        parser.add_option("-v", "--verbose",
                          action="store_true", default=False,
                          help="verbose yaml convertion")

        options, args = parser.parse_args()

        verbose = options.verbose

        if not args:
            raise HelpExit()

        if 2 != len(args):
            raise RuntimeError("two posiitonal arguments are expected")

        convert(*args, overwrite=options.force, verbose=options.verbose)

    except HelpExit:
        parser.print_help()

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
