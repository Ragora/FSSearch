"""
    Programming for the operator token.
"""

import re

from .word import Word
from .token import Token
from .string import String
from parse.operators import Operator

class ParenthesesOpen(Token):
    __PATTERN__ = re.compile("\(")
