# -*- coding: utf-8 -*-

"""Qurawl Level

Core game actions
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import defaultdict as defdict

####

import common.debugit as debugit
import common.graphs as graphs
import common.queues as queues
from qurawl.items import Corpse

####

__all__ = ['LevelMap', 'Level']

####

NO_DBG = []
dbg = debugit.Debugit(__name__, NO_DBG)

####

class LevelMap(object):
    """2 dim list of map tokens"""

    def __init__(self, level):

        self.level_map = list(map(list, level.split()))
        self.width = len(self.level_map[0])
        self.height = len(self.level_map)


    def __getitem__(self, xy):
        x, y = xy
        return self.level_map[y][x]

####

class Level(object):
    """
    Here is the action:
        - move
        - pick
        - drop
        - attack
    """

    def __init__(self, level_map, commenter, conf, **items):

        self.level_map = level_map
        actors = items['actors']
        monsters = items['monsters']
        things = items['things']
        self.actors = set(actors)
        self.monsters = set(monsters)
        acmo = actors + monsters
        self.coord_actors = dict(zip((actor.position for actor in acmo), acmo))
        self.coord_things = dict(zip((thing.position for thing in things), things))
        self.obstacles = items['obstacles']
        self.conf = conf

        self.future_moves = defdict(list)
        self.pos_move = dict()
        self.future_drops = defdict(list)
        self.future_attacks = defdict(list)
        self.commenter = commenter


    @property
    def width(self):

        return self.level_map.width


    @property
    def height(self):

        return self.level_map.height


    def is_valid_move(self, x, y):

        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        if self.level_map[x, y] in self.obstacles:
            return False

        return True


    def is_active(self, actor):

        return actor in self.coord_actors.itervalues()


    def filter_deads(self):

        deads = set(actor for actor in self.coord_actors.itervalues() if actor.is_dead)
        coac = self.coord_actors
        self.coord_actors = dict((pos, act) for pos, act in coac.iteritems()
                                 if act not in deads)

        dbg(7, deads, 'deads')
        return deads


    def move(self, actor, direct):

        if not self.is_active(actor):
            self.commenter(10, "{0} not active (move)".format(actor.name))
            return
        goal = actor.look(direct)
        if self.is_valid_move(*goal):
            self.future_moves[goal].append(actor)
            self.pos_move[actor.position] = goal


    def resolve_moves(self):

        move_multipos = defdict(list)
        for move, actors in self.future_moves.items():
            for actor in actors:
                move_multipos[move].append(actor.position)

        static = set(self.coord_actors) - set(self.pos_move)
        static |= self.propagate_static(move_multipos, static)

        doable = {}
        for move in move_multipos:
            if move not in static and self.level_map[move] not in self.obstacles:
                doable[move] = move_multipos[move]

        # handle free places
        movings = {}
        for move, positions in doable.items():
            if move not in self.pos_move and move not in static:
                sortpos = sorted(positions, key=lambda p: self.coord_actors[p].priority)
                movings[move] = sortpos[0]
                static.update(sortpos[1:])

        static |= self.propagate_static(doable, static)

        # handle occupied places
        beset = {}
        for move in set(doable) - set(movings):
            beset[move] = doable[move]

        for move, positions in beset.items():
            if move not in static:
                for pos in positions:
                    if move == self.pos_move[pos] and pos == self.pos_move[move]:
                        static.add(move)
                        static.add(pos)
                        break
                valid_pos = [p for p in positions if p not in static]
                if not valid_pos:
                    continue
                first = min(valid_pos, key=lambda p: self.coord_actors[p].priority)
                movings[move] = first
                static.update(set(valid_pos) - set([first]))

        static |= self.propagate_static(doable, static)
        real_moves = {}
        for move, pos in movings.items():
            if move not in static:
                real_moves[move] = self.coord_actors[pos]

        return real_moves


    def propagate_static(self, moves, static):

        visited = set()
        for move in moves:
            if move in static and move not in visited:
                visited |= graphs.dfs_connected(moves, move)

        return visited


    def drop(self, actor, name, direct):

        if not self.is_active(actor):
            self.commenter(10, "{0} not active (drop)".format(actor.name))
            return

        goal = actor.look(direct)
        if self.level_map[goal] not in self.obstacles:
            self.future_drops[goal].append((actor, name))
        else:
            self.commenter(2, "{0} can't drop {1} {2}.".format(actor.name, name, direct))



    def resolve_drops(self):

        valid_pos = set(self.future_drops) - \
          (set(self.coord_actors) | set(self.coord_things))
        for goal in valid_pos:
            actor, name = min(self.future_drops[goal], key=lambda x: x[0].priority)
            thing = actor.drop(name, *goal)
            if thing:
                self.coord_things[goal] = thing
                if thing.is_good:
                    actor.update_karma()
            else:
                self.commenter(2, "{0} can't drop {1}.".format(actor.name, name))
        self.future_drops = defdict(list)



    def pick_things(self, real_moves):

        pick_locs = set(real_moves) & set(self.coord_things)
        picks = set([])
        for pos in pick_locs:
            actor = self.coord_actors[pos]
            thing = self.coord_things[pos]
            result = actor.equip.pick(thing)
            if result > 0:
                picks.update([(result, actor, thing)])
                if result & 1:
                    self.coord_things.pop(pos)

        return picks


    def attack(self, actor, direct):

        if not self.is_active(actor):
            self.commenter(10, "{0} not active (attack)".format(actor.name))
            return

        goal = actor.look(direct)
        if self.level_map[goal] not in self.obstacles:
            self.future_attacks[goal].append(actor)


    def resolve_attacks(self):

        attacks = dict((self.coord_actors[pos], self.future_attacks[pos])
                       for pos in self.future_attacks if pos in self.coord_actors)
        pairs = graphs.node_pairs(attacks)
        queue = queues.PriorityQueue()
        queue.reset()
        queue.push_pairs(((a.attack_priority, d.attack_priority), (a, d))
                         for a, d in pairs)
        rounds = self.conf['rounds']
        dt = self.conf['dt']
        while len(queue) > 0:
            _, (attacker, defender) = queue.pop()
            fight(attacker, defender, dt, rounds)
            self.update_karma(attacker, defender)
            self.commenter.fight(attacker, defender)

        self.future_attacks = defdict(list)


    def update_karma(self, attacker, defender):

        if attacker in self.actors and defender in self.actors:
            if defender.is_dead:
                attacker.update_karma(0)
            else:
                attacker.update_karma(-1)
        else:
            if defender.is_dead:
                attacker.update_karma()
            if attacker.is_dead:
                defender.update_karma()


    def call_monsters(self):

        for monster in self.monsters:
            if self.is_active(monster):
                cmd = monster(level=self)
                if cmd:
                    verb, args = cmd[0], cmd[1:]
                    try:
                        getattr(self, verb)(monster, *args)
                    except AttributeError as ae:
                        dbg(10, ae, env=self.call_monsters)
                        pass


    def set_actors(self, moves):
        """Selectively update  actor, monster positions"""
        is_new = set()
        for new_position, actor in moves.items():
            # old position could be new position for another actor
            if actor.position not in is_new:
                self.coord_actors.pop(actor.position)
            actor.position = new_position
            is_new.add(new_position)
            self.coord_actors[new_position] = actor

        self.future_moves = defdict(list)
        self.pos_move = {}


    def set_corpses(self, deads):

        for actor in deads:
            self.coord_things[actor.position] = Corpse(actor)


    def action(self):

        self.call_monsters()
        real_moves = self.resolve_moves()
        self.set_actors(real_moves)
        picks = self.pick_things(real_moves)
        for res_act_thing in picks:
            self.commenter.pick(*res_act_thing)
        deads = self.filter_deads()
        self.resolve_drops()
        self.resolve_attacks()
        deads.update(self.filter_deads())
        self.set_corpses(deads)
        for actor in deads:
            self.commenter.dead(actor)


    def render(self, renderer):

        renderer.draw_terrain(self.level_map)
        map(renderer.draw_item, self.coord_things.itervalues())
        map(renderer.draw_item, self.coord_actors.itervalues())



    def _pr_future_moves(self, future_moves):

        for pos, acts in future_moves.items():
            print pos, acts
            for a in acts:
                print a.name, a.symbol,
            print


####

def fight(attacker, defender, dt, rounds=1):

    atta, defe = attacker, defender
    strikes = rounds
    # is_weak (=low strength)
    # => to little damage
    # => is_dead state possibly cannot be reached
    while strikes > 0 and not any((atta.is_weak, atta.is_dead, defe.is_dead)):
        dbg(6, strikes, 'strikes')
        attack_value = atta.attack_power()
        defend_value = defe.defend_power()
        dbg(6, attack_value, 'attack value')
        dbg(6, defend_value, 'defend value')
        attacker_damage = defend_value / (1 + attack_value)
        defender_damage = attack_value / (1 + defend_value)
        dbg(6, attacker_damage ,'attacker damage')
        dbg(6, defender_damage, 'defender damage')
        atta.set_damage(attacker_damage * dt)
        defe.set_damage(defender_damage * dt)
        atta, defe = defe, atta
        strikes -= 1

    return attacker.is_dead, defender.is_dead

####

