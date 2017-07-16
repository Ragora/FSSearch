"""
    Base logical operator class.
"""

class LogicalOperator(object):
    def evaluate(self, target_file, rhs=None):
        raise NotImplementedError(".evaluate not implemented.")
