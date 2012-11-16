#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test queues.py
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

import common.queues as queues

####

class TestPriorityQueue(ut.TestCase):


    def test_empty(self):

        pq = queues.PriorityQueue()
        self.assertEqual(len(pq), 0)
        self.assertEqual(pq.pop(), None)

         
    def test_pushpop1(self):

        pair = (3, 1)
        pq = queues.PriorityQueue()

        pq.push_pairs([pair])
        self.assertEqual(len(pq), 1)
        self.assertEqual(pq.pop(), pair)
        self.assertEqual(pq.pop(), None)


    def test_pushpop3(self):

        pairs = [(3, 1), (2, 2), (1, 3)]
        pq = queues.PriorityQueue()
        pq.push_pairs(pairs)

        self.assertEqual(len(pq), len(pairs))
        for pair in sorted(pairs):
            self.assertEqual(pq.pop(), pair)
        self.assertEqual(pq.pop(), None)


    def test_remove(self):

        pairs = [(3, 1), (2, 2), (1, 3)]
        pq = queues.PriorityQueue()
        pq.push_pairs(pairs)
        pq.remove(2)

        self.assertEqual(len(pq), len(pairs) - 1)
        self.assertEqual(pq.pop(), pairs[2])
        self.assertEqual(pq.pop(), pairs[0])
        self.assertEqual(pq.pop(), None)

####

if __name__ == '__main__':

    ut.main()
