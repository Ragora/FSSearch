"""
    Filesystem searching software. This software acts as both a library and
    an independent program used to provide search queries to your file system
    and return the results to either the terminal or the calling python
    programming.

    Copyright (C) 2017 Robert MacGregor

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
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
        return "<%f %s Ago>" % (self.total_time, self.time_unit)

    def is_operator(self, target_file, rhs):
        start_date = self.payload(target_file)
        end_date = datetime.datetime
        return True

    def payload(self, target_file):
        if self.__UNITS__[self.time_unit.upper()] is None:
            invocation = {"%ss" % self.time_unit.lower(): self.total_time}
            return datetime.datetime.now() - datetime.timedelta(**invocation)
        invocation = {"days": self.total_time * self.__UNITS__[self.time_unit.upper()]}
        return datetime.datetime.now() - datetime.timedelta(**invocation)
