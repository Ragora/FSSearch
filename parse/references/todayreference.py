"""
    Today reference programming.
"""

import datetime

from .reference import Reference

class TodayReference(Reference):
    __TOKEN__ = "TODAY"

    def payload(self, target_file):
        return datetime.datetime.now()
