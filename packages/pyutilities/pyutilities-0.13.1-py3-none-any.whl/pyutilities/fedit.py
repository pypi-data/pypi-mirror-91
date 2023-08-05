#!/usr/bin/env python
# coding=utf-8

"""
    Inplace/inline file editing utility.

    Created:  Gusev Dmitrii, 13.04.2017
    Modified: Gusev Dmitrii, 04.03.2019
"""

# todo: implement: add line mode (if not found needed line)

import sys
import fileinput
import argparse

# - string checking types
CHECK_TYPE_STARTS = 'starts'
CHECK_TYPE_ENDS = 'ends'
CHECK_TYPE_CONTAINS = 'contains'
CHECK_TYPES = (CHECK_TYPE_STARTS, CHECK_TYPE_ENDS, CHECK_TYPE_CONTAINS)


def check_str(check_type, source_str, test_str):
    """
    Check relation between string and test string, according to test type
    :param check_type: type of matching
    :param source_str: string for test
    :param test_str: testing string
    :return:
    """
    if check_type == CHECK_TYPE_STARTS:
        return source_str.startswith(test_str)
    elif args.edit_type == CHECK_TYPE_ENDS:
        return source_str.endswith(test_str)
    elif args.edit_type == CHECK_TYPE_CONTAINS:
        return test_str in source_str


# create arguments parser
parser = argparse.ArgumentParser(description='File editing tool: replace inline values.')
# add arguments to parser (mandatory/optional)
parser.add_argument('-f', '--file',      dest='infile',    action='store',
                    required=True, help='file to change inline')
parser.add_argument('-s', '--sourceStr', dest='sourceStr', action='store',
                    required=True, help='source string for change')
parser.add_argument('-d', '--destStr',   dest='destStr',   action='store',
                    required=True, help='target string for change')
# optional
parser.add_argument('-t', '--type',      dest='edit_type', action='store',
                    choices=CHECK_TYPES, default=CHECK_TYPE_STARTS,
                    help='type of inline edit')
# parse cmd line parameters
args = parser.parse_args()

# inplace file processing
# todo: refactor edit logic into function
# todo: add some checks - file existence, etc
for line in fileinput.input(files=[args.infile], inplace=True, backup='.original'):
    # if we found string - we will replace it
    if check_str(args.edit_type, line, args.sourceStr):
        sys.stderr.write("Found: {}\n".format(args.sourceStr))
        print(args.destStr)
    else:
        print(line,)
