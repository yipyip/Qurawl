# -*- coding: utf-8 -*-

"""Command Line View

The view in MVC.
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import sys
import os
from collections import defaultdict as defdict

####

from common.environ import ENV
import qurawl.regparse as rp

####

__all__ = ['CliView']

####

CODING = ENV['encoding']

####

write_encode = lambda s: sys.stdout.write(s.encode(CODING))
input_encode = lambda prompt="-> ": raw_input(prompt).decode(CODING)
nl = lambda: write_encode(os.linesep)

####

class CliView(object):
    """Console UI"""

    def __init__(self, controller, engine, renderer, conf):

        self.controller = controller
        self.renderer = renderer(engine, conf)
        self.loop_reset()
        self.forms = {'health':   "[Health{0:>5}]",
                      'armor':    "[Armor{0:>5}]",
                      'strength': "[Strength{0:>5}]",
                      'karma':    "[Karma{0:>5}]",
                      'mine':     "[Mines{0:>5}]"}
        self.order = ('health', 'armor', 'strength', 'karma', 'mine')


    def loop_reset(self):

        self.stats_buf = []
        self.coms_buf = []


    def format_actor_stats(self, name, args, kwargs):

        value_form = " ".join(self.forms[k].format(int(kwargs[k]))\
                              for k in self.order if k in kwargs)
        single_form = " ".join("<{0}>".format(arg) for arg in args)
        return "{0:>8} {1} {2}".format(name, value_form, single_form)


    def set_actor_stats(self, stats):

        self.stats_buf.extend(self.format_actor_stats(name, args, kwargs)\
                              for name, args, kwargs in stats)


    def write_actor_stats(self):

        for stat in self.stats_buf:
            write_encode(stat)
            nl()


    def set_comments(self, coms):

        self.coms_buf.extend("-< {0}".format(com) for com in coms)


    def write_comments(self):

        for com in self.coms_buf:
            write_encode(com)
            nl()


    def get_input(self):

        tokens = map(lambda t: t.lower(), input_encode().split())

        if len(tokens) == 0:
            return 'ret', {}

        if tokens[0] in ('q', 'quit', 'exit'):
            return 'quit', {}

        return 'cmd', tokens


    def render(self, obj):

        obj.render(self.renderer)


    def run(self):

        running = True
        meta_info, tokens = 'ret', {}
        while running:
            self.loop_reset()
            running = self.controller.process(meta_info, tokens)
            self.renderer.display()
            nl()
            self.write_actor_stats()
            self.write_comments()
            if running:
                meta_info, tokens = self.get_input()
        nl()

####
