"""
    A base class representing an operand.
"""

class Operand(object):
    def payload(self, target_file):
        raise NotImplementedError(".payload() is not implemented on '%s'" % self.__class__.__name__)
