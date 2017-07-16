"""
    KiloBytes suffix programming.
"""

from .suffix import Suffix

class KiloBytes(Suffix):
    __TOKEN__ = "KB"

    def mutate(self, input):
        return input * 1000
