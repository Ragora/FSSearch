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

class SyntaxError(CompilerError):
    def __init__(self, token_index, previous_token, expected, found, query=None, message=None):
        if type(expected) is not list and expected is not None:
            expected = [expected]

        # Produce the base message
        expected = " or ".join([expected_class.__name__ for expected_class in expected])
        base_message = "Syntax error in query (at token index %u, character %u)" % (token_index, found.match_data.start())
        if message is None:
            message = base_message + ". Expected: %s after %s ('%s'). " % (expected, type(previous_token).__name__, previous_token.match_data.group(0))
        else:
            message = base_message + ": '%s'. Expected: %s after %s ('%s'). " % (message, expected, type(previous_token).__name__, previous_token.match_data.group(0))

        message += "Found: %s ('%s')" % (type(found).__name__, found.match_data.group(0))

        # Then highlight the error
        if query is not None:
            message += "\n\nIn query:\n%s\n" % query
            message += "".join(["-"] * found.match_data.start()) + "^"

        # Make it easier to read
        message = "\n\n%s\n" % message
        super(SyntaxError, self).__init__(message)
