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

class Operand(object):
    """
        Base class for all operands in the parsed structure. Operands are used to provide payoad data to
        the operators that are used to produce search results on a per-file basis.
    """

    def payload(self, target_file):
        """
            Returns the payload associated with this operand.

            :param target_file: The TargetFile instance that this operand is being used on.
        """
        raise NotImplementedError(".payload() is not implemented on operand '%s'" % self.__class__.__name__)
