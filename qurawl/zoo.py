# -*- coding: utf-8 -*-

"""Qurawl Actors and Inventory Playground
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import itertools as it
import random as rand

####

import common.debugit as debugit
from qurawl.level import *
from qurawl.items import *

####

NO_DBG = []
dbg = debugit.Debugit(__name__, NO_DBG)

####

SINGLE_EQUIP = set(('silver_key', 'gold_key'))
VALUE_EQUIP  = set(('health', 'armor', 'strength', 'karma', 'mine'))

MAXIMA = {'health': 100, 'armor': 100, 'strength': 100}
EQUIPMENT = {'health': 100, 'armor': 10, 'strength': 50, 'karma': 5}
THINGS = {'health': ('+', 'health', 5, 6),
          'armor': (']', 'armor', 5, 6),
          'strength': ('!', 'strength', 5, 6),
          'silver_key': ('%', 'silver_key', 1, 1),
          'gold_key': ('$', 'gold_key', 1, 1)}

DEF_EQUIP = MAXIMA, EQUIPMENT, VALUE_EQUIP, SINGLE_EQUIP

####

def make_level(rows, cols):

    row0 = ["#" * cols]
    return "\n".join(row0 + [("." * (cols-2)).join("##")] * rows + row0)

####

class Cycler(Monster):


    def __init__(self, name, symbol, x, y, priority, cmds, equip=None, factory=None):

        super(Cycler, self).__init__(name, symbol, x, y, priority, equip, factory)
        self.cmd_cycle = it.cycle(cmds)


    def cycle(self, steps=0):
        """Shift cycle state"""
        for _ in xrange(steps):
            cmd = self.cmd_cycle.next()
    

    def __call__(self, **kwargs):

        return self.cmd_cycle.next()
        

####

class Randomer(Monster):


    def __init__(self, name, symbol, x, y, priority, cmds, equip=None, factory=None):

        super(Randomer, self).__init__(name, symbol, x, y, priority, equip, factory)
        self.cmds = cmds


    def __call__(self, **kwargs):

        cmd = rand.choice(self.cmds)
        dbg(7, cmd, 'randomer:')
        return cmd

####

class Marauder(Monster):


    def __init__(self, name, symbol, x, y, priority, equip=None, factory=None):

        super(Marauder, self).__init__(name, symbol, x, y, priority, equip, factory)


    def __call__(self, **args):

        level = args['level']
        directs = 'up', 'left', 'down', 'right'
        for d in directs:
            pos = self.look(d)
            if pos in level.coord_actors and not self.is_weak:
                return 'attack', d

        return ['move', rand.choice(directs)]

####

def make_yip(x, y, priority):

    equipment = Equipment(*DEF_EQUIP)
    factory = ThingFactory(Thing, THINGS)
    return Actor('yip', 'Y', x, y, priority, equipment, factory)

####

def make_otto(x, y, priority):

    equipment = Equipment(*DEF_EQUIP)
    factory = ThingFactory(Thing, THINGS)
    return Actor('otto', 'O', x, y, priority, equipment, factory)


####

def make_xenia(x, y, priority):

    equipment = Equipment(*DEF_EQUIP)
    factory = ThingFactory(Thing, THINGS)
    return Actor('xenia', 'X', x, y, priority, equipment, factory)

####

def make_minelayer(x, y, priority, n):

    equip = {'health': 100, 'armor': 40, 'strength': 50, 'mine': 100}
    things = {'mine': ('*', 'health', -10, 1)}

    raw_cmds = ('move down', 'drop mine left') * n +\
               ('move right', 'drop mine down') * n +\
               ('move up', 'drop mine right') * n +\
               ('move left', 'drop mine up') * n

    cmds = [c.split() for c in raw_cmds]
    equipment = Equipment(MAXIMA, equip, VALUE_EQUIP, SINGLE_EQUIP)
    factory = ThingFactory(Thing, things)
    return Cycler('minelayer', 'm', x, y, priority, cmds, equipment, factory)

####

def make_fighter(x, y, priority):

    equip = {'health': 50, 'armor': 0, 'strength': 40}
    raw_cmds = ('attack left',)
    cmds = [c.split() for c in raw_cmds]
    equipment = Equipment(MAXIMA, equip, *DEF_EQUIP[2:])
    factory = ThingFactory(Thing, THINGS)
    return Cycler('left attacker', 'f', x, y, priority, cmds, equipment, factory)

####

def make_marauder(x, y, priority):

    equipment = Equipment(*DEF_EQUIP)
    name = 'marauder_{0}{1}'.format(x, y)
    return Marauder(name, 'r', x, y, priority, equipment)


####

def make_marauder_column(x, y, priority, n):

    return [make_marauder(x, y+i, priority+i) for i in xrange(0, 2*n, 2)]

####

def make_cyclers(x, y, priority):

    equip = {'health': 20, 'armor': 0, 'strength': 30}
    i_cxy = enumerate(zip("abcd", (0, 0, 1, 1), (0, 1, 1, 0)))
    cmds = [c.split() for c in ("move down", "move right", "move up", "move left")]

    cyclers = []
    for i, (char, dx, dy) in i_cxy:
        equipment = Equipment(MAXIMA, equip, *DEF_EQUIP[2:])
        cyclers.append(Cycler('cycler_{0}'.format(char), char,
                              x+dx, y+dy, priority+i, cmds, equipment))

    for i, cycler in enumerate(cyclers):
        cycler.cycle(i)
    return cyclers

####
# Args: <name> <symbol> <x> <y> <which attribute to update> <value> <pickable or not>
make_acid = lambda x, y: Thing('acid', '~', 'health', x, y, -3, False)
make_trap = lambda x, y: Thing('trap', '^', 'health', x, y, -4, False)
make_health = lambda x, y: Thing('health', '+', 'health', x, y, 5)
make_armor = lambda x, y: Thing('armor', ']', 'armor', x, y, 10)
make_strength = lambda x, y: Thing('strength', '!', 'strength', x, y, 12)
make_silver_key = lambda x, y: Thing('silver_key', '%', 'silver_key', x, y)
make_gold_key = lambda x, y: Thing('gold_key', '$', 'gold_key', x, y)

####

def make_actors():

    return (make_yip(3, 8, 0),
            make_otto(3, 10, 1),
            make_xenia(3, 12, 2))

####

def make_monsters():

    monsters = (make_minelayer(19, 6, 4, 7),
                make_fighter(5, 10, 5))

    cyclers = make_cyclers(6, 13, 11)
    marauders = make_marauder_column(15, 2, 12, 10)
    return monsters + tuple(cyclers) + tuple(marauders)

####

def make_things():

    return (make_acid(4, 5),
            make_acid(5, 5),
            make_trap(5, 6),
            make_health(7, 11),
            make_health(8, 11),
            make_strength(9, 11),
            make_armor(10, 13),
            make_silver_key(11, 14),
            make_gold_key(12, 14),
            make_health(7, 16),
            make_strength(8,16),
            make_armor(9, 16))

####
