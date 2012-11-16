# -*- coding: utf-8 -*-

"""Graph Algorithms"""

####

from __future__ import absolute_import
from __future__ import unicode_literals

####

__all__ = ['dfs_connected', 'node_pairs']

####

def dfs_connected(graph, start):
    """Find nodes in connected subgraph with node 'start'

    Args:
        graph:
             An instance of dict.
        start:
             A key in graph.

    Returns:
        visited:
            A set of nodes.
    """
    assert isinstance(graph, dict), 'Not a Graph'
    assert start in graph, 'not start node'

    stack = [start]
    visited = set()
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            # ask for permission because it can be a defaultdict!
            # (no try, except)
            if node in graph:
                next_nodes = graph[node]
                stack.extend(next_nodes)

    return visited

####

def node_pairs(graph):
    """Collect 'from-to' nodes in directed graph

    Args:
        graph:
             An instance of dict.
        
    Returns:
        pairs:
            A list of node pairs.
    """

    stack = []
    pairs = []
    visited = set()

    for vertex in graph:
        stack.append(vertex)
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                # ask for permission because it can be a defaultdict!
                # (no try, except)
                if node in graph:
                    next_nodes = graph[node]
                    stack.extend(next_nodes)
                    # save reverse direction
                    for other in next_nodes:
                        pairs.append((other, node))

    return pairs

####
