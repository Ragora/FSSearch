"""
    Programming for the word token.
"""

import re

from .token import Token

class Word(Token):
    __PATTERN__ = re.compile("([A-z]+)")
