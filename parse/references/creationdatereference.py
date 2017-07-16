"""
    Contents reference programming.
"""

from .reference import Reference

class CreationDateReference(Reference):
    __TOKEN__ = "CREATION DATE"

    def payload(self, target_file):
        return target_file.creation_date
