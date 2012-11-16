# -*- coding: utf-8 -*-

"""Qurawl Main"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import itertools as it
import random as rand
import difflib as diff

####

import common.debugit as debugit
import qurawl.regparse as rp
from qurawl.level import *
from qurawl.items import *
import qurawl.zoo as zoo

####

__all__ = ['Qurawl', 'Commenter']

####

NO_DBG = []
MONSTERS = [6]
dbg = debugit.Debugit(__name__, NO_DBG) #MONSTERS)

####

OBSTACLES    = ('#',)

#### Word Categories

names   = set(['yip', 'otto', 'xenia'])
verbs   = set(['move', 'attack', 'use', 'push'])
obverbs = set(['drop'])
objects = set(['health', 'armor', 'strength', 'mine', 'silver_key', 'gold_key'])
directs = set(['up', 'left', 'right', 'down'])

# Lookup table (word -> Category)
LEXICON = rp.make_lexicon((names, verbs, obverbs, objects, directs), 'NVWOD')

####

class Qurawl(object):
    """Main Game Class"""

    def __init__(self, conf, lexicon=LEXICON):

        seed = conf['seed']
        if seed > 0:
            rand.seed(seed)
        self.conf = conf
        self.lexicon = lexicon
        self.commenter = Commenter()


    def init_all(self):

        level_map = LevelMap(zoo.make_level(20, 30))
        actors = zoo.make_actors()
        self.act_level = Level(level_map, self.commenter, self.conf,
                               actors=actors, monsters=zoo.make_monsters(),
                               things=zoo.make_things(), obstacles=OBSTACLES)
        self.name_actors = dict(zip((actor.name for actor in actors), actors))


    def start(self):

        self.init_all()


    @property
    def level(self):

        return self.act_level


    def input_action(self, tokens):

        scan_info = fuzzy_scan(tokens, self.lexicon)
        dbg(4, scan_info, 'scan info', self.input_action)
        if 'err' in scan_info:
            self.commenter(1, "Don't know {0}.".format(scan_info['err']))
            return

        parse_info = rp.parse_nvod(scan_info['match'], self.lexicon)
        dbg(4, parse_info, 'parse info', self.input_action)
        if 'err' in parse_info:
            self.commenter(1, "Don't know what to do: {0}".\
              format(show_parse_errors(parse_info['err'])))
            return

        cmd = make_command(parse_info)
        verb, args = cmd[0], cmd[1:]
        try:
            action_method = getattr(self.level, verb)
        except AttributeError:
            self.commenter(1, "Don't know how to '{0}'!".format(verb))
            return

        for name in parse_info['name']:
            action_method(self.name_actors[name], *args)


    def action(self, meta_info):

        self.level.action()
        if 'quit' == meta_info:
            self.fin()


    def get_actor_stats(self):

        dbg(6, [m.stat for m in self.level.monsters])
        return [actor.stat for actor in self.level.actors if not actor.is_dead]


    def get_comments(self):

        return self.commenter.show(100)


    def loop_reset(self):

        self.commenter.reset()


    def fin(self):

        self.commenter(1, "Bye")

####

class Commenter(object):
    """Collect and return state and action comments"""

    def __init__(self):

        self.reset()


    def reset(self):

        self.buf = []


    def __call__(self, level, msg):

        self.buf.append((level, msg))


    def __iter__(self):

        return iter(self.buf)


    def pick(self, result, actor, thing):

        if isinstance(thing, Corpse):
            com = "{0} plunders the corpse of {1}."
            name = thing.name.rsplit("_", 1)[0]
            self.buf.append((2, com.format(actor.name, name)))
            return

        if result < 2:
            com = "{0} picked up {1}({2})."
        else:
            com = "{0} is hurt by {1}({2})."
        self.buf.append((3, com.format(actor.name, thing.name, thing.value)))


    def dead(self, actor):

        com = "{0} is dead, sigh!".format(actor.name)
        self.buf.append((2, com))


    def fight(self, attacker, defender):

        com = "{0} attacks {1}!".format(attacker.name, defender.name)
        self.buf.append((2, com))


    def show(self, level):

        return (msg for i, msg in self if i <= level)

####

def show_parse_errors(pairs):
    """Gather invalid command infos."""
    return " ".join(word if categ != "?" else categ for categ, word in pairs)

####

def make_command(parse_info, phrases=('verb', 'obverb', 'object', 'direct')):
    """Reconstruct a valid command."""
    # use verb 'move' as default
    # check if (ob)verb is already existent
    use_move = bool(set(('verb', 'obverb')) & set(parse_info))
    info = dict(parse_info, **({'verb': 'move'}, {})[use_move])

    return [info[key] for key in phrases if key in info]

####

def fuzzy_scan(words, lexicon):
    """Check if words have a resonable similarity to lexicon words."""
    matches = [diff.get_close_matches(word, lexicon, n=1) for word in words]
    if not all(matches):
        return {'err': " ".join(w for w, m in zip(words, matches) if not m)}
    else:
        return {'match': list(it.chain(*matches))}

####
