# -*- coding: utf-8 -*-

"""Qurawl Item, Actor, Equipment, Thing,...
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict as defdict
import itertools as it
import random as rand

####

import common.debugit as debugit

####

__all__ = ['Item', 'Actor', 'Monster', 'Equipment',
           'Thing', 'ThingFactory', 'Corpse']

####

NO_DBG = []
dbg = debugit.Debugit(__name__, NO_DBG)

####

rand01 = rand.random

#####

def const_factory(value=0):

    return it.repeat(value).next

####

class Item(object):
    """Something that has a name and a position"""

    def __init__(self, name, symbol, x, y):

        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y


    @property
    def position(self):

        return self.x, self.y


    @position.setter
    def position(self, xy):

        self.x, self.y = xy


    def __repr__(self):

        return "{0} {1} {2} {3}".format(self.name, self.symbol, self.x, self.y)

####

class Actor(Item):
    """
    An Item with equipmet and optional dropping feature
    """
    moves = {'up': (0, -1), 'left': (-1, 0), 'down': (0, 1), 'right': (1, 0)}
    weak = 10
    dead = 20

    def __init__(self, name, symbol, x, y, priority, equip, factory=None):

        super(Actor, self).__init__(name, symbol, x, y)
        self.priority = priority
        self.equip = equip
        self.factory = factory


    def look(self, direct):

        dx, dy = Actor.moves[direct]
        return self.x + dx, self.y + dy


    def drop(self, name, x, y):

        if self.factory:
            portion = self.factory.get_portion(name)
            if portion is not None:
                if self.equip.drop(name, portion):
                    return self.factory(name, x, y)


    @property
    def stat(self):

         return (self.name,) + self.equip.stat


    @property
    def attack_priority(self):

        return self.equip['karma']


    def attack_power(self):

        return self.equip.attack_power()


    def defend_power(self):

        return self.equip.defend_power()


    def set_damage(self, damage):

        self.equip.set_damage(damage)


    @property
    def is_weak(self):

        return self.equip['strength'] < self.weak


    @property
    def is_dead(self):

        return self.equip['health'] < self.dead


    def update_karma(self, value=1):

        if value:
            dbg(7, value, 'value')
            karma = self.equip['karma'] + value
            self.equip['karma'] = max(0, min(karma, self.equip.refval))
        else:
            self.equip['karma'] = 0

        dbg(7, self.equip['karma'], 'e karma')


    def __repr__(self):

        return "{0} {1} {2} {3} {4}".format(self.name, self.symbol, self.x, self.y,
                                            self.priority)

####

class Monster(Actor):
    """
    An Actor which generates his own commands

    Function '__call__' must be implemented
    """
    def __call__(self, **args):
        """
        Args:
            args: Informations for specific behaviour
                  Used keys are:
                      step (see Cycler in zoo.py)
                      vel (see level.call_monsters in level.py)

        Returns:
            Command sequence
            (Example: ['move', 'up'])
        """
        pass

####

class Equipment(object):
    """Attributes and inventory of an actor"""

    refval = 100.0

    def __init__(self, maxima, equip, value_slots, single_slots):

        self.maxima = defdict(const_factory(1))
        self.maxima.update(maxima)
        self.equip = defdict(const_factory(0))
        self.equip.update(equip)
        self.value_slots = value_slots
        self.single_slots = single_slots
        self.slots = value_slots | single_slots


    def pick(self, thing):
        """Let thing do the stuff."""

        if isinstance(thing, Corpse) or thing.equitem in self.slots:
            return thing.update(self.equip, self.maxima)
        return False


    def drop(self, name, portion=1):

        if name in self.slots:
            if self.equip[name] >= portion:
                self.equip[name] -= portion
                return True
        return False


    @property
    def stat(self):

        equip = self.equip
        single_keys = set(equip) & self.single_slots
        value_keys = set(equip) & self.value_slots
        # show if > 0
        single_equip = sorted([key for key in single_keys if equip[key]])
        value_equip = dict((key, equip[key]) for key in value_keys)
        return single_equip, value_equip


    def attack_power(self):

        strength = self.equip['strength'] / self.refval
        health = self.equip['health']  / self.refval
        return strength * health


    def defend_power(self):

        armor = self.equip['armor'] / self.refval
        health = self.equip['health'] / self.refval
        return armor * health


    def set_damage(self, damage):

        def delta(attr, damage):
            return attr * damage * rand01()

        attributes = 'health', 'armor', 'strength'
        equip = self.equip
        for attr in attributes:
            equip[attr] -= delta(equip[attr], damage)


    def reset(self):

        self.equip = defdict(const_factory(0))


    def __getitem__(self, name):

        return self.equip[name]


    def __setitem__(self, name, value):

        self.equip[name] = value


    def __iter__(self):

        return iter(self.equip)


    def __repr__(self):
        return ' '.join("{0}={1}".format(key, value) for key, value in\
                        sorted(self.equip.iteritems()))

####

class Thing(Item):
    """Something that lays around"""

    def __init__(self, name, symbol, equitem, x, y, value=1, pickable=True):

        super(Thing, self).__init__(name, symbol, x, y)
        self.equitem = equitem
        self.value = value
        self.pickable = pickable


    def update(self, equip, maxima):
        """Universal update:
        - increase value or
        - inflict damage
          of equipment 'equitem'.

        Results:
            true : Thing is picked up.
            false: Thing remains untouched.
        """
        equitem = self.equitem
        equipval = equip[equitem]
        maximum = maxima[equitem]
        if self.value > 0:
            if equipval < maximum:
                equip[equitem] = min(equipval + self.value, maximum)
                return 1
            else:
                return 0
        else:
            equip[equitem] = max(0, equipval + self.value)
            return 2 + self.pickable

    @property
    def is_good(self):

        return self.value > 0


    def __repr__(self):

        return super(Thing, self).__repr__() +\
          " {0} {1} {2}".format(self.equitem, self.value, self.pickable)

####

class ThingFactory(object):
    """Facilitate dropping of things"""

    def __init__(self, klass, thing_defs):

        self.funcs = {}
        self.portions = {}
        for name, (sym, equitem, value, portion) in thing_defs.iteritems():
            self.funcs[name] = self.create(klass, name, sym, equitem, value)
            self.portions[name] = portion


    def create(self, klass, name, sym, equitem, value):

        return lambda x, y: klass(name, sym, equitem, x, y, value)


    def get_portion(self, name):

        return self.portions.get(name, None)


    def __call__(self, name, *args, **kwargs):

        return self.funcs.get(name, lambda *args, **kwargs: None)(*args, **kwargs)

####

class Corpse(Item):
    """A dead actor which can be picked up"""

    def __init__(self, actor):

        x, y = actor.position
        super(Corpse, self).__init__('{0}_corpse'.format(actor.name), "?", x, y)
        self.actor = actor


    def update(self, equip, maxima):

        corpse_equip = self.actor.equip
        # take the remaining values...
        for attr in ('health', 'armor', 'strength'):
            equip[attr] = min(equip[attr] + corpse_equip[attr], maxima[attr])
        # ...and his inventory
        # Game Logic Attention!
        # There shouldn't be multiple single-items of one kind.
        # If corpse and plunderer share the same single item, 1 item vanishes.
        for equitem in corpse_equip.single_slots:
            if corpse_equip[equitem]:
                equip[equitem] = 1
        dbg(7, equip, 'corpse')
        corpse_equip.reset()
        # thing compatible
        return 1


    def __repr__(self):

        return 'corpse {0}'.format(repr(self.actor))

####

