# -*- coding: utf-8 -*-

"""Parser for the regular language:
S -> N D
S -> N V D
S -> N V O D

Abbrev:
N := name(s)
D := direction
V := verb
W := verb with object
O := object
"""

####

from __future__ import absolute_import
from __future__ import unicode_literals
import re
import itertools as it

####

__all__ = ['make_lexicon', 'parse_nvod']

####

def make_lexicon(phrases, tags):

    words_tag = lambda (words, tag): ((w, tag) for w in words)
    tagged = it.imap(words_tag, zip(phrases, tags))
    return dict(it.chain(*tagged))

####

def parse_nvod(words, lexicon, with_name=True):
    """Simple Parser based on regex ^N*(D|VD|VOD)$ .

    Returns:
        Args:
            words:
                List of lowercase words
            lex:
                Dict of word:category items
            with_name:
               Mandatory or optional actor names
        Result:
            Dict of Command elements if success
            Dict with key 'err' and list of regex and input informations if error
    """

    verbose_keys = {"N":"name", "V":"verb", "W": "obverb",
                    "O": "object", "D":"direct"}
    # 0 or more names | 1 or more names
    regex = r'^(N{0})(D|VD|WOD)$'.format(('*', '+')[with_name])
    pat = re.compile(regex)
    expr = ''.join(lexicon.get(w, '?') for w in words)
    matched = pat.match(expr)

    if matched:
        # Always store name(s) in list.
        result = {'N': []}
        iwords = iter(words)
        for key in matched.group(1):
            result[key].append(iwords.next())
        for key in matched.group(2):
            result[key] = iwords.next()
        return dict((verbose_keys[key], val) for key, val in result.iteritems())

    return {'err': [(verbose_keys.get(key, key), w) for key, w in zip(expr, words)]}

####
