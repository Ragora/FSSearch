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

from .compilererror import CompilerError

class UnknownOperatorError(CompilerError):
    """
        An error representing an unknown operator. This should not be thrown under normal circumstances.
    """

    def __init__(self, token_index, previous_token, current_token, query, operator):
        message = "Unknown operator '%s' in query (at token index %u, character %u)\n\n" % (operator, token_index, current_token.match_data.start())
        message += "In query:\n %s\n" % query
        message += "".join(["-"] * current_token.match_data.start()) + "^"

        super(UnknownOperatorError, self).__init__(message)
