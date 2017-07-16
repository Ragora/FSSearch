"""
    Contents reference programming.
"""

from .reference import Reference

class ContentsReference(Reference):
    __TOKEN__ = "CONTENTS"

    def payload(self, target_file):
        return target_file.contents
