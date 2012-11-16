# -*- coding: utf-8 -*-

"""Simple Debug Handling"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import sys
import os

####

class Debugit(object):
    """Debugging output controlled by numbers"""

    def __init__(self, name, groups, write=sys.stdout.write, nl=os.linesep):

        self.name = name if name else __name__
        self.groups = groups
        self.write = write
        self.nl = nl


    def __call__(self, group, obj, com='', env=None):

        if group in self.groups:
            if hasattr(env, '__name__'):
                msg = env.__name__
            else:
                msg = self.name

            self.write("[{0}] {1}: ".format(msg, com))

            if isinstance(obj, dict):
                self.write("{0}{1}".format(type(obj), self.nl))
                for key in obj:
                    self.write("{0}={1}{2}".format(key, obj[key], self.nl))
            elif hasattr(obj, '__iter__'):
                self.write("{0}{1}".format(type(obj), self.nl))
                for item in obj:
                    self.write("{0}{1}".format(item, self.nl))
            else:
                self.write("{0} {1}{2}".format(type(obj), obj, self.nl))

####
