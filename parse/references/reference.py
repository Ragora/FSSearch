"""
    Base reference class programming.
"""

import parse

class Reference(parse.Operand):
    def __init__(self, match_data):
        pass
        
    def evaluate(self, target_file, rhs=None):
        return True
