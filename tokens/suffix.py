"""
    Class for suffix programming.
"""

import re

from .token import Token
from parse.suffixes import Suffix as SuffixBase

class Suffix(Token):
    __OPERATORS__ = {operator.__name__: operator for operator in SuffixBase.__subclasses__()}
    __PATTERN__ = re.compile("(%s)" % "|".join(["(?:%s)" % operator.__TOKEN__ for operator in SuffixBase.__subclasses__()]))
