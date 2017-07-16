"""
    Python programming for the and operator.
"""

from .logicaloperator import LogicalOperator

class AndOperator(LogicalOperator):
    __TOKEN__ = "AND"

    def evaluate(self, target_file, rhs=None):
        if rhs is not None:
            return target_file and rhs
        return self.lhs.evaluate(target_file) and self.rhs.evaluate(target_file)
