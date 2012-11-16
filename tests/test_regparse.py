#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test regparse.py
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import unittest as ut

####

try:
    # as main
    import paths
except ImportError:
    # as module
    pass

import qurawl.regparse as rp

####

class TestRegparse(ut.TestCase):


    def setUp(self):

        names = set(['yip', 'otto', 'xenia'])
        verbs = set(['move', 'attack'])
        obverbs = set(['drop'])
        objects = set(['health', 'armor'])
        directs = set(['up', 'left', 'right', 'down'])

        self.lexicon = rp.make_lexicon((names, verbs, obverbs, objects, directs),
                                       ('N', 'V', 'W', 'O', 'D'))


    def check(self, result, keys, values):

        self.assertEqual(set(result), set(keys))
        for i, key in enumerate(keys):
            self.assertEqual(result[key], values[i])


    def check_err(self, result):

        self.assertEqual(set(result), set(['err']))


    def test_valid_cmds(self):

        cmd = ['yip', 'move', 'up']
        result = rp.parse_nvod(cmd, self.lexicon, with_name=1)
        self.check(result, ['name', 'verb', 'direct'], [['yip']] + cmd[1:])


        cmd = ['xenia', 'drop', 'health', 'left']
        result = rp.parse_nvod(cmd, self.lexicon, with_name=1)
        self.check(result, ['name', 'obverb', 'object', 'direct'],
                   [['xenia']] + cmd[1:])

        cmd = ['xenia', 'yip', 'down']
        result = rp.parse_nvod(cmd, self.lexicon, with_name=1)
        self.check(result, ['name', 'direct'], [['xenia', 'yip']] + cmd[2:])

        cmd = ['up']
        result = rp.parse_nvod(cmd, self.lexicon, with_name=0)
        self.check(result, ['name', 'direct'], [[]] + cmd)

        cmd = ['drop', 'armor', 'right']
        result = rp.parse_nvod(cmd, self.lexicon, with_name=0)
        self.check(result, ['name', 'obverb', 'object', 'direct'], [[]] + cmd)


    def test_invalid_cmds(self):

         self.check_err(rp.parse_nvod([], self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod([], self.lexicon, with_name=0))

         cmd = ['up', 'attack', 'yip']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))

         cmd = ['a', 'b', 'c', 'd', 'e']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))

         cmd = ['yip']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))

         cmd = ['move']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))

         cmd = ['up']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))

         cmd = ['a', 'b', 'c', 'd', 'e']
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))
         
         cmd = xrange(8)
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=1))
         self.check_err(rp.parse_nvod(cmd, self.lexicon, with_name=0))

####

if __name__ == '__main__':

    ut.main()
