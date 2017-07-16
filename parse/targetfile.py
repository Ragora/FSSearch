"""
    A class representing a targeted file.
"""

import os
import datetime

class TargetFile(object):
    path = None
    """
        The path to the targeted file.
    """

    size = None
    """
        The size of the file in bytes.
    """

    creation_date = None
    """
        The date the file was created on.
    """

    def __init__(self, path):
        self.path = path

        # FIXME: Allow for processing bits of files at a time
        with open(path, "rb") as handle:
            self.contents = handle.read()

        self.size = os.path.getsize(path)
        self.creation_date = datetime.datetime.fromtimestamp(os.path.getctime(path))
