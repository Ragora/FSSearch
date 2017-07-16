"""
    Suffix base class.
"""

class Suffix(object):
    def mutate(self, input):
        raise NotImplementedError(".mutate is not implemented on '%s'." % self.__class__.__name__)
