#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test graphs.py
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

import common.graphs as graphs

####

class TestConnected(ut.TestCase):


    def test_nograph(self):

        self.assertRaises(AssertionError, graphs.dfs_connected, None, 1)
        self.assertRaises(AssertionError, graphs.dfs_connected, 'graph', None)


    def test_notstart(self):

        self.assertRaises(AssertionError, graphs.dfs_connected, {1:[2]}, 2)
        self.assertRaises(AssertionError, graphs.dfs_connected, {1:[2]}, 3)


    def test_subgraph(self):

        graph = {1: [2], 2: [1, 3], 4: [5]}
        visited = set([1, 2, 3])
        self.assertEqual(visited, graphs.dfs_connected(graph, 1))

        graph = {2: [1], 3: [2], 1: [3]}
        visited = set([1, 2, 3])
        self.assertEqual(visited, graphs.dfs_connected(graph, 2))

        graph = {1: [2, 3], 3: [4], 4: [1], 5: [6]}
        visited = set([1, 2, 3, 4])
        self.assertEqual(visited, graphs.dfs_connected(graph, 3))


####

class TestNodePairs(ut.TestCase):


    def test_emptygraph(self):

        graph = {}
        pairs = []
        self.assertEqual(pairs, graphs.node_pairs(graph))


    def test_pairs(self):

        graph = {2: [1], 3: [2], 1: [3]}
        visited = set([(1, 2), (2, 3), (3, 1)])
        self.assertEqual(visited, set(graphs.node_pairs(graph)))

        graph = {1: [2, 3], 3: [4], 4: [1], 5: [6]}
        visited = set([(2, 1), (3, 1), (4, 3), (1, 4), (6, 5)])
        self.assertEqual(visited, set(graphs.node_pairs(graph)))
        
####

if __name__ == '__main__':

    ut.main()
