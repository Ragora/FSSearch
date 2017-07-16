"""
    Filename reference programming.
"""

import os

from .reference import Reference

class FileNameReference(Reference):
    __TOKEN__ = "FILENAME"

    def payload(self, target_file):
        return os.path.basename(target_file.path)
