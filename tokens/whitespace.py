"""
    Programming for the whitespace token.
"""

import re

from .token import Token

class WhiteSpace(Token):
    __PATTERN__ = re.compile("( +)")
