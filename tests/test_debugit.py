#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test debugit.py
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

import common.debugit as debug

####

class TestDebugit(ut.TestCase):


    def setUp(self):

        self.reset()


    def write(self, item):

        self.buf.append(item)


    def reset(self):

        self.buf = []


    def test_level(self):

        dbg = debug.Debugit('levels', [], write=self.write)
        dbg(1, 'nil', 'not written')
        self.assertEqual(self.buf, [])
        self.reset()

        dbg = debug.Debugit('levels', [1, 2], write=self.write)
        dbg(1, 10, 'com1')
        dbg(2, 20, 'com2')
        dbg(3, 30, 'com3')
        buf = [item.strip() for item in self.buf]
        self.assertEqual(buf, ['[levels] com1:', "<type 'int'> 10",
                               '[levels] com2:', "<type 'int'> 20"])
        self.reset()


    def test_list(self):

        dbg = debug.Debugit('alist', [1], write=self.write)
        dbg(1, [1,2], '12')
        buf = [item.strip() for item in self.buf]
        self.assertEqual(buf, ['[alist] 12:', "<type 'list'>",  '1', '2'])
        self.reset()


    def test_dict(self):

        dbg = debug.Debugit('adict', [1], write=self.write)
        dbg(1, {'x': 1, 'y': 2}, 'xy12')
        buf = [item.strip() for item in self.buf]
        head, tail = buf[:2], buf[2:]
        self.assertEqual(head, ['[adict] xy12:', "<type 'dict'>"])
        self.assertEqual(set(tail), set(['x=1', 'y=2']))
        self.reset()

####

if __name__ == '__main__':

    ut.main()
