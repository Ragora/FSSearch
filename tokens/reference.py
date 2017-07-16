"""
    Class for the logical operator programming.
"""

import re

from .token import Token
from parse.references import Reference

class Reference(Token):
    __OPERATORS__ = {operator.__name__: operator for operator in Reference.__subclasses__()}
    __PATTERN__ = re.compile("(%s)" % "|".join(["(?:%s)" % operator.__TOKEN__ for operator in Reference.__subclasses__()]), re.IGNORECASE)
