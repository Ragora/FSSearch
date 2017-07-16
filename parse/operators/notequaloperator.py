"""
    Base operator class.
"""

from .operator import Operator

class NotEqualOperator(Operator):
    __TOKEN__ = "!="
