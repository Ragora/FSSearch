"""
    Base operator class.
"""

import re

from .operator import Operator

class MatchesPatternOperator(Operator):
    __TOKEN__ = "MATCHES PATTERN"

    def evaluate(self, target_file):
        lhs_payload = self.lhs.payload(target_file)

        match_result = re.match(self.rhs.payload(target_file), lhs_payload)
        if match_result is None:
            return False
        return (match_result.end() - match_result.start()) == len(lhs_payload)
