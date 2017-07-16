"""
    Programming for the word token.
"""

import re

from .token import Token
from .suffix import Suffix
from .logicaloperator import LogicalOperator

class Number(Token):
    __EXPECTS__ = [Suffix, LogicalOperator]
    __PATTERN__ = re.compile("([0-9]+)")
