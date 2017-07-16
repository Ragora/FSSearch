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

import os

import parse
from searchresult import SearchResult

class SearchQuery(object):
    """
        A class representing an executable search query.
    """

    def evaluate(self, target_file):
        return self._execute(target_file, self.compiled_data)

    def _execute(self, target_file, target_code):
        logic_results = [(logical_operator.evaluate(target_file), logical_operator) for logical_operator in target_code]
        current_evaluation, _ = logic_results[0]

        for current_boolean, logical_operator in logic_results:
            # FIXME: Represent single-component queries without having this hack here
            if type(logical_operator) in parse.operators.Operator.__subclasses__():
                current_evaluation = current_boolean
                break
            current_evaluation = logical_operator.evaluate(current_evaluation, current_boolean)

            # FIXME: Implement on the operator itself
            if type(logical_operator) is parse.logic.OrOperator and current_evaluation is True:
                return True
        return current_evaluation

    def execute(self, path=os.getcwd()):
        """
            Executes the search query.
        """

        # Collect a file list first (so we can use multiprocessing later)
        file_list = []
        for directory, directory_names, filenames in os.walk(path):
            for filename in filenames:
                relative_path = os.path.join(directory, filename)

                if os.path.isfile(relative_path):
                    file_list.append(parse.TargetFile(relative_path))

        # Process the file list
        matched_files = []
        for current_file in file_list:
            result = self._execute(current_file, self.compiled_data)
            if result is True:
                matched_files.append(SearchResult(path=current_file.path))

        return matched_files

    def optimize(self):
        """
            Optimizes the query for performance. This is mostly useful when processing large sets of files.

            :FIXME: This is currently a stub.
        """

    def __init__(self, compiled_data):
        self.trace = []
        self.compiled_data = compiled_data

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
