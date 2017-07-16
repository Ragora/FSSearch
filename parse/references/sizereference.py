"""
    Size reference programming.
"""

from .reference import Reference

class SizeReference(Reference):
    __TOKEN__ = "SIZE"

    def payload(self, target_file):
        return target_file.size
