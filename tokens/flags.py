"""
    Programming for the flag token.
"""

import re

from .token import Token
from .reference import Reference

class Flags(Token):
    __PATTERN__ = re.compile("([A-z]+(,[A-z]+)*):")
