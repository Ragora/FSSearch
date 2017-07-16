"""
    Programming for the number AST Element.
"""

from .dataelement import DataElement

class Number(DataElement):
    suffix = None
    """
        The suffix that was supplied.
    """

    number = None
    """
        The number value.
    """

    def __init__(self, number, suffix):
        self.suffix = suffix
        self.number = float(number)

    def payload(self, target_file):
        return self.number if self.suffix is None else self.suffix.mutate(self.number)
