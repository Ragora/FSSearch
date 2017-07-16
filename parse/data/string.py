"""
    Programming for the string data element.
"""

from .dataelement import DataElement

class String(DataElement):
    string = None
    """
        The string data that was supplied.
    """

    def __init__(self, string):
        self.string = string

    def payload(self, target_file):
        return self.string
