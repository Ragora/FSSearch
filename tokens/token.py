"""
    Base token class.
"""

class Token(object):
    def __init__(self, match_data):
        self.match_data = match_data

    def __str__(self):
        return "<%s token: %s>" % (self.__class__.__name__, repr(self.match_data.group(0)))
