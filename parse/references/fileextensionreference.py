"""
    File extension reference programming.
"""

import os

from .reference import Reference

class FileExtensionReference(Reference):
    __TOKEN__ = "(?:FILE)? EXTENSION"

    def payload(self, target_file):
        built_extension = ""
        current_extension = "Initial"
        current_path = os.path.basename(target_file.path)

        while current_extension != "":
            current_path, current_extension = os.path.splitext(current_path)
            built_extension += current_extension
        return built_extension
