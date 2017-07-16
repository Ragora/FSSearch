"""
    Base operator class.
"""

import re

from .operator import Operator

class ContainsWildcardOperator(Operator):
    __TOKEN__ = "CONTAINS WILDCARD"

    def evaluate(self, target_file):
        # FIXME: This is a hack implementation that will break
        rhs_payload = self.rhs.payload(target_file).replace("*", ".*?")

        return re.match(rhs_payload, self.lhs.payload(target_file)) is not None
