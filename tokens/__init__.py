"""
    Main import script for the tokens.
"""

from .word import Word
from .flags import Flags
from .token import Token
from .suffix import Suffix
from .number import Number
from .string import String
from .operator import Operator
from .reference import Reference
from .whitespace import WhiteSpace
from .parenthesesopen import ParenthesesOpen
from .logicaloperator import LogicalOperator
from .parenthesesclose import ParenthesesClose

SYNTAX_TABLE = {
    # For now, only operators with two parameters
    LogicalOperator: [Reference, ParenthesesOpen],
    Operator: [Word, String, Number, Reference],
    Number: [LogicalOperator, Suffix],
    Reference: [Operator, LogicalOperator],
    String: [LogicalOperator, ParenthesesClose],
    Suffix: [LogicalOperator],
    Flags: [Reference],
    Word: [String, Number],
    ParenthesesClose: [ParenthesesClose, LogicalOperator],
    ParenthesesOpen: [ParenthesesOpen, Reference]
}
