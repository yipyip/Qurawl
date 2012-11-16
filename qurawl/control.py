#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Controller

The C in MVC.
"""

###

from __future__ import absolute_import
from __future__ import unicode_literals
import sys
import os

####

try:
    # as main
    import paths
except ImportError:
    # as module
    pass

from common.environ import ENV
from qurawl.engines.charengine import CharEngine
from qurawl.charqurawl import CharQurawl
from qurawl.cliview import CliView
import qurawl.qurawl as qurawl

####

__all__ = ['Controller']

####

class Controller(object):
    """Entry Point to run the game"""
    
    def __init__(self, game, view, engine, renderer, conf):

        self.game = game(conf)
        self.view = view(self, engine, renderer, conf)
        self.game.start()


    def process(self, meta_info, tokens):

        self.game.loop_reset()
        if meta_info not in ('ret', 'quit'):
            self.game.input_action(tokens)

        self.game.action(meta_info)
        self.view.render(self.game.level) # abstraction?!
        stats = self.game.get_actor_stats()
        self.view.set_actor_stats(stats)
        self.view.set_comments(self.game.get_comments())

        if 'quit' == meta_info:
            return False
        return True


    def run(self):

        self.view.run()

####

CONFIG = {'seed': 0,
          'rounds': 2,
          'dt': 0.9}
####

def main(conf):

    Controller(qurawl.Qurawl, CliView, CharEngine, CharQurawl, conf).run()
    return 0

####

if __name__ == '__main__':
    """Application call with default configuration"""
    sys.exit(main(CONFIG))

####

