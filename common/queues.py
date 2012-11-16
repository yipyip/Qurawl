# -*- coding: utf-8 -*-

"""Queue like Data Structures"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import heapq as hq

####

class PriorityQueue(object):

    def __init__(self):

        self.reset()

    
    def reset(self):

        self.queue = []
        self.entry_finder = {}    


    def push_pairs(self, pairs):

        for priority, item in pairs:
            self.push(item, priority)


    def push(self, item, priority=0):

        if item in self.entry_finder:
            self.remove(item)

        entry = [priority, item]
        self.entry_finder[item] = entry
        hq.heappush(self.queue, entry)


    def remove(self, item):

        entry = self.entry_finder.pop(item)
        entry[-1] = None


    def pop(self):

        while self.queue:
            priority, item = hq.heappop(self.queue)
            if item is not None:
                self.entry_finder.pop(item)
                #return item
                return priority, item
        return None


    def __len__(self):

        # not self.queue!
        return len(self.entry_finder)

####



