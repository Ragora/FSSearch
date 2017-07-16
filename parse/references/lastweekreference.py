"""
    Last week reference programming.
"""

from .reference import Reference

class LastWeekReference(Reference):
    __TOKEN__ = "LAST WEEK"

    def payload(self, target_file):
        return datetime.datetime.now() - datetime.timedelta(days=7)
