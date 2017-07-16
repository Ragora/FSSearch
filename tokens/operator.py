"""
    Programming for the operator token.
"""

import re

from .word import Word
from .token import Token
from .string import String
from parse.operators import Operator

class Operator(Token):
    __OPERATORS__ = {operator.__name__: operator for operator in Operator.__subclasses__()}
    __PATTERN__ = re.compile("(%s)" % "|".join(["(?:%s)" % operator.__TOKEN__ for operator in Operator.__subclasses__()]), re.IGNORECASE)
