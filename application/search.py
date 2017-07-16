#!/usr/bin/python
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
import os
import sys
import datetime

from querycompiler import QueryCompiler

class Application(object):
    """
        Main application object.
    """

    def main(self):
        query = None
        filepath = None

        if len(sys.argv) == 2:
            query = sys.argv[1]
            filepath = os.getcwd()
        elif len(sys.argv) == 3:
            query = sys.argv[2]
            filepath = sys.argv[1]

        if query is None or filepath is None:
            print("Usage: %s <filepath/query> [query]" % sys.argv[0])
            return

        compiler = QueryCompiler()
        query = compiler.compile(query)

        results = query.iexecute(path=filepath)
        # Execute search
        #self.results_start = datetime.datetime.now()
        #results = self.execute(parsed_ast)
        #self.results_end = datetime.datetime.now()

        # Produce timing output
        """
        if self.timed:
            compile_delta = compile_end - compile_start
            parse_delta = parse_end - parse_start
            results_delta = results_end - results_start
            print("=========================================================")
            print("Compiled in: %s" % str(compile_delta))
            print("Parsed in: %s" % str(parse_delta))
            print("Results in: %s" % str(compile_delta))
            print("Total: %s" % (compile_delta + parse_delta + results_delta))
            print("=========================================================")
        """

        # Produce results
        for result in results:
            print(result.path)

if __name__ == "__main__":
    Application().main()
