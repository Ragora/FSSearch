"""
    Base operator class.
"""

from .operator import Operator

class EqualsOperator(Operator):
    __TOKEN__ = "==?"

    def evaluate(self, target_file):
        return self.lhs.payload(target_file) == self.rhs.payload(target_file)
