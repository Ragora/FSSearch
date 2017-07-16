"""
    Programming for the string token.
"""

import re

from .token import Token
from .logicaloperator import LogicalOperator

class String(Token):
    __PATTERN__ = re.compile("('|\")(.*?)\\1")
