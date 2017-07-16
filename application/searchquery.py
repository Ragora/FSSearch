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
import time
import random
import multiprocessing

import parse
from searchresult import SearchResult

def _threaded_execute(target_data):
    """
        Internal threaded execution function. This is used when thread counts are not None.

        :param target_data: A tuple (SearchQuery, TargetFile).

        :return: A list of TargetFile objects that match the search term.
        :rtype: list
    """
    built_query, target_file = target_data
    return built_query.execute([target_file], thread_count=None)

class SearchQuery(object):
    """
        A class representing an executable search query.
    """

    # FIXME: We should signify this from the base class that has .evaluate
    def evaluate(self, target_file):
        return self._execute(target_file, self.compiled_data)

    def _execute(self, target_file, target_code):
        """
            Internal executor function. This is what actually implements the search query execution logic.

            :param target_file: The current TargetFile object we are processing.
            :param target_code: The current query code to execute. We don't use self.compiled_data directly because we handled
                parentheses by recursively nesting queries.
        """
        logic_results = [(logical_operator.evaluate(target_file), logical_operator) for logical_operator in target_code]
        current_evaluation, _ = logic_results[0]

        for current_boolean, logical_operator in logic_results:
            # FIXME: Represent single-component queries without having this hack here
            if type(logical_operator) in parse.operators.Operator.__subclasses__():
                current_evaluation = current_boolean
                break
            current_evaluation = logical_operator.evaluate(current_evaluation, current_boolean)

            if logical_operator.__SHORT_CIRCUIT__ is not None:
                # If the short circuit is a boolean, then we return if the current result is equal
                if type(logical_operator.__SHORT_CIRCUIT__) is bool and logical_operator.__SHORT_CIRCUIT__ is current_evaluation:
                    return current_evaluation
                # If the short circuit is anything else, it's a callable function.
                elif type(logical_operator.__SHORT_CIRCUIT__) is not bool and logical_operator.__SHORT_CIRCUIT__(current_evaluation) is True:
                    return current_evaluation
        return current_evaluation

    def execute(self, target=os.getcwd(), thread_count=multiprocessing.cpu_count()):
        """
            Executes the search query.

            :param target: If a string, it is the target directory to recurse. If a list, it is either a list of strings representing
                the files to process or TargetFile instances.
            :param thread_count: The number of threads to use when processing the query. This defaults to the number of available processing
                cores the executing system has. If None, then the query is processed in this thread. This uses the multiprocessing module internally,
                so you actually get concurrent processing.

            :return: A list of SearchResult objects.
            :rtype: list
        """

        # Collect a file list first (so we can use multiprocessing later)
        file_list = target if type(target) is list else []
        if type(target) is not list:
            for directory, directory_names, filenames in os.walk(target):
                for filename in filenames:
                    relative_path = os.path.join(directory, filename)

                    if os.path.isfile(relative_path):
                        file_list.append(parse.TargetFile(relative_path))
        else:
            file_list = [parse.TargetFile(file_entry) if type(file_entry) is str else file_entry for file_entry in file_list]

        matched_files = []
        if thread_count is None:
            # Process the file list
            for current_file in file_list:
                result = self._execute(current_file, self.compiled_data)
                if result is True:
                    matched_files.append(SearchResult(path=current_file.path))
        else:
            thread_pool = multiprocessing.Pool(thread_count)
            passed_data = [(self, current_file) for current_file in file_list]

            result_files = thread_pool.imap(_threaded_execute, passed_data)
            for result in result_files:
                matched_files += result

        return matched_files

    def iexecute(self, path=os.getcwd(), thread_count=8):
        """
            Executes the search query and returns an iterator to results from the query. This allows you to execute queries asynchronously and retrieve results
            as they become available.

            :param target: If a string, it is the target directory to recurse. If a list, it is either a list of strings representing
                the files to process or TargetFile instances.
            :param thread_count: The number of threads to use when processing the query. This defaults to the number of available processing
                cores the executing system has. If None, then the query is processed in this thread. This uses the multiprocessing module internally,
                so you actually get concurrent processing.

            :return: A generator to the results of the query.
            :rtype: generator
        """

        # Collect a file list first (so we can use multiprocessing later)
        file_list = path if type(path) is list else []
        if type(path) is not list:
            for directory, directory_names, filenames in os.walk(path):
                for filename in filenames:
                    relative_path = os.path.join(directory, filename)

                    if os.path.isfile(relative_path):
                        file_list.append(parse.TargetFile(relative_path))

        if thread_count is None:
            for current_file in file_list:
                result = self._execute(current_file, self.compiled_data)
                if result is True:
                    yield SearchResult(path=current_file.path)
        else:
            thread_pool = multiprocessing.Pool(thread_count)
            passed_data = [(self, current_file) for current_file in file_list]

            result_files = thread_pool.imap(_threaded_execute, passed_data)
            for result_list in result_files:
                for result in result_list:
                    yield result

    def optimize(self):
        """
            Optimizes the query for performance. This is mostly useful when processing large sets of files.

            :FIXME: This is currently a stub.
        """

    def __init__(self, compiled_data):
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
