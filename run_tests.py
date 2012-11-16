#!/usr/bin/env python

"""Calling all UnitTests"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import sys
import os
import glob
import unittest as ut

####

test_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), "tests")
sys.path.insert(0, test_path)
test_files = glob.glob(os.path.join(test_path, "test_*.py"))
test_names = [os.path.basename(tf)[:-3] for tf in test_files]

####

def main():

    suite = ut.defaultTestLoader.loadTestsFromNames(test_names)
    result = ut.TextTestRunner(sys.stderr, verbosity=2).run(suite)
    return 0

####

if __name__ == '__main__':
    sys.exit(main())







