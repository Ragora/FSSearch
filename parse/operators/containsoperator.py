"""
    Base operator class.
"""

from .operator import Operator

class ContainsOperator(Operator):
    __TOKEN__ = "CONTAINS"

    def evaluate(self, target_file):
        return self.rhs.payload(target_file) in self.lhs.payload(target_file)
