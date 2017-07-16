"""
    Python programming for the and operator.
"""

from .logicaloperator import LogicalOperator

class OrOperator(LogicalOperator):
    __TOKEN__ = "OR"

    def evaluate(self, target_file, rhs=None):
        if rhs is not None:
            return target_file or rhs
        return self.lhs.evaluate(target_file) or self.rhs.evaluate(target_file)
