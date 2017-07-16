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

import re

from .token import Token
from .reference import Reference
from parse.logic import LogicalOperator

class LogicalOperator(Token):
    """
        Logical operators are the boolean arithmetic operators that are used to combine search terms in meaningful
        ways for the search executor to handle.
    """

    __OPERATORS__ = {operator.__name__: operator for operator in LogicalOperator.__subclasses__()}
    """
        A dictionary mapping operator tokens to the operator classes supported by the program. They are built automatically from Python's reflection.
    """

    __PATTERN__ = re.compile("(%s)" % "|".join(["(?:%s)" % operator.__TOKEN__ for operator in LogicalOperator.__subclasses__()]), re.IGNORECASE)
    """
        A regular expression pattern automatically built from the operator list.
    """
