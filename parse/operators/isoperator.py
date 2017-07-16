"""
    Base operator class.
"""

from .operator import Operator

class IsOperator(Operator):
    __TOKEN__ = "IS"

    def evaluate(self, target_file):
        return self.lhs.payload(target_file) > self.rhs.payload(target_file)
