"""
    Class for the logical operator programming.
"""

import re

from .token import Token
from .reference import Reference
from parse.logic import LogicalOperator

class LogicalOperator(Token):
    __OPERATORS__ = {operator.__name__: operator for operator in LogicalOperator.__subclasses__()}
    __PATTERN__ = re.compile("(%s)" % "|".join(["(?:%s)" % operator.__TOKEN__ for operator in LogicalOperator.__subclasses__()]), re.IGNORECASE)
