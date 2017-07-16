"""
    Days ago reference programming.
"""

import datetime

from .reference import Reference

class AgoReference(Reference):
    __UNITS__ = {
        "DAY": None,
        "HOUR": None,
        "SECOND": None,
        "MONTH": 30,
        "YEAR": 365,
        "WEEK": None
    }

    __TOKEN__ = "([0-9]+(?:\.[0-9]+)?) (%s)S? AGO" % "|".join(["(?:%s)" % current_unit for current_unit in __UNITS__.keys()])

    total_time = None
    """
        The total time ago.
    """

    time_unit = None
    """
        The time unit that is being used.
    """

    def __init__(self, match_data):
        self.time_unit = match_data.group(3)
        self.total_time = float(match_data.group(2))

    def __repr__(self):
        return "<%f Days Ago>" % self.total_days

    def payload(self, target_file):
        if self.__UNITS__[self.time_unit.upper()] is None:
            invocation = {"%ss" % self.time_unit.lower(): self.total_time}
            return datetime.datetime.now() - datetime.timedelta(**invocation)
        invocation = {"days": self.total_time * self.__UNITS__[self.time_unit.upper()]}
        return datetime.datetime.now() - datetime.timedelta(**invocation)
