"""
    Base operator class.
"""

import re

from .operator import Operator

class ContainsPatternOperator(Operator):
    __TOKEN__ = "CONTAINS PATTERN"

    def evaluate(self, target_file):
        return re.search(self.rhs.payload(target_file), self.lhs.payload(target_file)) is not None
