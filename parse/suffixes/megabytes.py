"""
    Megabytes suffix programming.
"""

from .suffix import Suffix

class MegaBytes(Suffix):
    __TOKEN__ = "MB"

    def mutate(self, input):
        return input * 1000000
