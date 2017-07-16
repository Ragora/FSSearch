"""
    Base operator class.
"""

class Operator(object):
    def evaluate(self, target_file):
        raise NotImplementedError(".evaluate not implemented on '%s'" % self.__class__.__name__)
