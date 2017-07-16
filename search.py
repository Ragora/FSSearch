#!/usr/bin/python
import re
import os
import sys
import datetime

import parse
import tokens

TOKENS = [
    tokens.Flags,
    tokens.String,
    tokens.Reference,
    tokens.Suffix,
    tokens.LogicalOperator,
    tokens.Operator,
    tokens.Word,
    tokens.Number,
    tokens.ParenthesesClose,
    tokens.ParenthesesOpen,
    tokens.WhiteSpace
]

def push_tokens(pushed_tokens, token_stream):
    pushed_tokens = [pushed_tokens] if type(pushed_tokens) is not list else pushed_tokens

    for pushed_token in pushed_tokens:
        yield pushed_token
    for token in token_stream:
        yield token

def generate_token_stream(input):
    current_character_position = 0

    current_index = 0
    while current_index != len(input):
        for token_data in TOKENS:
            match_data = token_data.__PATTERN__.match(input, current_index)

            if match_data is not None:
                found_match = True
                yield token_data(match_data)
                current_index = match_data.end()
                break
        else:
            raise StandardError("No token read.")

class QueryError(StandardError):
    pass

class SyntaxError(QueryError):
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

class UnknownOperatorError(QueryError):
    """
        An error representing an unknown operator. This should not be thrown under normal circumstances.
    """

    def __init__(self, token_index, previous_token, current_token, query, operator):
        message = "Unknown operator '%s' in query (at token index %u, character %u)\n\n" % (operator, token_index, current_token.match_data.start())
        message += "In query:\n %s\n" % query
        message += "".join(["-"] * current_token.match_data.start()) + "^"

        super(UnknownOperatorError, self).__init__(message)

class UnknownLogicalOperatorError(QueryError):
    """
        An error representing an unknown logical operator. This should not be thrown under normal circumstances.
    """

    def __init__(self, token_index, previous_token, current_token, query, operator):
        message = "Unknown logical operator '%s' in query (at token index %u, character %u)\n\n" % (operator, token_index, current_token.match_data.start())
        message += "In query:\n %s\n" % query
        message += "".join(["-"] * current_token.match_data.start()) + "^"

        super(UnknownLogicalOperatorError, self).__init__(message)

class UnknownReferenceError(QueryError):
    """
        An error representing an unknown reference. This should not be thrown under normal circumstances.
    """

    def __init__(self, token_index, previous_token, current_token, query, reference):
        message = "Unknown reference '%s' in query (at token index %u, character %u)\n\n" % (reference, token_index, current_token.match_data.start())
        message += "In query:\n %s\n" % query
        message += "".join(["-"] * current_token.match_data.start()) + "^"

        super(UnknownReferenceError, self).__init__(message)

class BadParenthesesError(QueryError):
    """
        An error representing an unknown reference. This should not be thrown under normal circumstances.
    """

    def __init__(self):
        super(BadParenthesesError, self).__init__("Bad parentheses.")

class SearchQuery(object):
    timed = False
    """
        Whether or not the search should be timed. This is a debugging tool.
    """

    def handle_timed_flag(self):
        self.timed = True

    def handle_verbose_flag(self):
        pass

    FLAG_HANDLERS = {
        "timed": handle_timed_flag,
        "verbose": handle_verbose_flag,
    }

    current_compilation = None
    """
        The current compilation result.
    """

    previous_token = None

    logic_stack = None
    """
        A list of list references that contains where in the logic stack we are.
    """

    def handle_flags_token(self, index, token, token_stream, query):
        flags = token.match_data.group(1).split(",")

        # Must be the first index
        if index != 0:
            raise SyntaxError(expected=[])

        called_functions = []
        for current_flag in flags:
            current_flag = current_flag.lower()

            if current_flag not in self.FLAG_HANDLERS:
                raise SyntaxError(expected=[])
            else:
                called_functions.append(self.FLAG_HANDLERS[current_flag])

        # Call the flag handlers
        for called_function in called_functions:
            called_function(self)

        return token_stream

    def handle_string_token(self, index, token, token_stream, query):
        self.logic_stack[-1].append(parse.data.String(string=token.match_data.group(2)))
        return token_stream

    def handle_whitespace_token(self, index, token, token_stream, query):
        return token_stream

    def handle_word_token(self, index, token, token_stream, query):
        print(token)
        return token_stream

    def handle_operator_token(self, index, token, token_stream, query):
        next_token = None

        # Read all operator components
        operator_components = [token.match_data.group(1)]
        while next_token is None or type(next_token) is tokens.Word or type(next_token) is tokens.WhiteSpace:
            next_token = next(token_stream)

            if type(next_token) is tokens.Word:
                operator_components.append(next_token.match_data.group(1))

        # Lookup the operator
        operator_token = " ".join(operator_components).rstrip().lstrip()
        operator_token_search = operator_token.lower()
        for operator_class in parse.operators.Operator.__subclasses__():
            current_operator_token = operator_class.__TOKEN__
            current_operator_match = re.match(re.compile(current_operator_token, re.IGNORECASE), operator_token_search)
            if current_operator_match is not None and (current_operator_match.end() - current_operator_match.start()) == len(operator_token_search):
                new_operator = operator_class()
                self.logic_stack[-1].append(new_operator)
                break
        else:
            raise UnknownOperatorError(token_index=index, previous_token=self.previous_token, current_token=token, query=query, operator=operator_token)

        if next_token is not None:
            return push_tokens(next_token, token_stream)
        return token_stream

    def handle_number_token(self, index, token, token_stream, query):
        number = token.match_data.group(1)
        self.logic_stack[-1].append(parse.data.Number(number=number, suffix=None))
        return token_stream

    def handle_logical_token(self, index, token, token_stream, query):
        operator_token = token.match_data.group(1)
        operator_token_search = operator_token.lower()
        for operator_class in parse.logic.LogicalOperator.__subclasses__():
            if operator_class.__TOKEN__.lower() == operator_token_search:
                new_operator = operator_class()
                self.logic_stack[-1].append(new_operator)
                break
        else:
            raise UnknownOperatorError(token_index=index, previous_token=self.previous_token, current_token=token, query=query, operator=operator_token)
        return token_stream

    def handle_suffix_token(self, index, token, token_stream, query):
        suffix_token = token.match_data.group(1)
        suffix_token_search = suffix_token.lower()
        for suffix_class in parse.suffixes.Suffix.__subclasses__():
            if suffix_class.__TOKEN__.lower() == suffix_token_search:
                new_suffix = suffix_class()
                self.logic_stack[-1].append(new_suffix)
                break
        else:
            raise UnknownReferenceError(token_index=index, previous_token=self.previous_token, current_token=token, query=query, operator=suffix_token)
        return token_stream

    def handle_reference_token(self, index, token, token_stream, query):
        reference_token = token.match_data.group(1)
        reference_token_search = reference_token.lower()
        for reference_class in parse.references.Reference.__subclasses__():
            reference_token = reference_class.__TOKEN__.lower()

            reference_match = re.match(re.compile(reference_token, re.IGNORECASE), reference_token_search)
            if reference_match is not None and (reference_match.end() - reference_match.start()) == len(reference_token_search):
                new_reference = reference_class(match_data=token.match_data)
                self.logic_stack[-1].append(new_reference)
                break
        else:
            raise UnknownReferenceError(token_index=index, previous_token=self.previous_token, current_token=token, query=query, operator=reference_token)
        return token_stream

    def handle_parentheses_close_token(self, index, token, token_stream, query):
        if len(self.logic_stack) == 1:
            raise BadParenthesesError()
        self.logic_stack.pop()
        return token_stream

    def handle_parentheses_open_token(self, index, token, token_stream, query):
        new_group = []
        self.logic_stack[-1].append(new_group)
        self.logic_stack.append(new_group)
        return token_stream

    TOKEN_HANDLERS = {
        tokens.Flags: handle_flags_token,
        tokens.String: handle_string_token,
        tokens.WhiteSpace: handle_whitespace_token,
        tokens.LogicalOperator: handle_logical_token,
        tokens.Word: handle_word_token,
        tokens.Operator: handle_operator_token,
        tokens.Number: handle_number_token,
        tokens.Suffix: handle_suffix_token,
        tokens.ParenthesesOpen: handle_parentheses_open_token,
        tokens.ParenthesesClose: handle_parentheses_close_token,
        tokens.Reference: handle_reference_token
    }

    def compile(self, query):
        self.current_compilation = []
        self.logic_stack = [self.current_compilation]

        token_stream = generate_token_stream(query)

        last_token = None

        try:
            current_index = 0
            current_stream = token_stream
            while True:
                current_token = next(current_stream)

                current_token_type = type(current_token)
                if current_token_type is tokens.WhiteSpace:
                    current_index += 1
                    continue

                if current_token_type not in self.TOKEN_HANDLERS:
                    raise QueryError("Unknown token type: %s" % current_token.__class__.__name__)

                # Check if it makes syntactically sense
                if self.previous_token is not None:
                    previous_token_type = type(self.previous_token)

                    expected_tokens = tokens.SYNTAX_TABLE[previous_token_type]
                    if current_token_type not in expected_tokens:
                        raise SyntaxError(expected=expected_tokens, query=query, previous_token=self.previous_token, found=current_token, token_index=current_index)

                self.previous_token = current_token
                current_stream = self.TOKEN_HANDLERS[current_token_type](self, current_index, current_token, token_stream, query)
                current_index += 1
        except StopIteration as e:
            pass
        return self.current_compilation

    def parse(self, compiled_data):
        """
            The final parse function. We assume the data is in the correct form and assemble it into the final executable
            format.
        """
        current_data = None
        current_operator = None

        produced_ast = []

        # First pass: Match suffixes to numbers
        removed_entries = []
        for index, current_element in enumerate(compiled_data):
            current_element_type = type(current_element)

            # If we have a number, look for a suffix
            if index < len(compiled_data) - 1 and current_element_type is parse.data.Number:
                next_element = compiled_data[index + 1]

                if type(next_element) in parse.suffixes.Suffix.__subclasses__():
                    current_element.suffix = next_element
                    removed_entries.append(next_element)
        produced_ast = [current_element for current_element in compiled_data if current_element not in removed_entries]

        # Second pass: Match data to their operators
        removed_entries = []
        for index, current_element in enumerate(produced_ast):
            current_element_type = type(current_element)

            if current_element_type in parse.operators.Operator.__subclasses__():
                current_element.lhs = produced_ast[index - 1]
                current_element.rhs = produced_ast[index + 1]
                removed_entries.append(current_element.lhs)
                removed_entries.append(current_element.rhs)
        produced_ast = [current_element for current_element in produced_ast if current_element not in removed_entries]

        # Third pass: Match logical operands
        removed_entries = []
        for index, current_element in enumerate(produced_ast):
            current_element_type = type(current_element)

            if current_element_type in parse.logic.LogicalOperator.__subclasses__():
                current_element.lhs = produced_ast[index - 1]
                current_element.rhs = produced_ast[index + 1]
                removed_entries.append(current_element.lhs)
                removed_entries.append(current_element.rhs)
        produced_ast = [current_element for current_element in produced_ast if current_element not in removed_entries]
        return produced_ast

    def execute(self, parsed_data, path=os.getcwd()):
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
            current_evaluation = True
            logic_results = [(logical_operator.evaluate(current_file), logical_operator) for logical_operator in parsed_data]
            for current_boolean, logical_operator in logic_results:
                if type(logical_operator) in parse.operators.Operator.__subclasses__():
                    current_evaluation = current_boolean
                    break

                current_evaluation = logical_operator.evaluate(current_evaluation, current_boolean)

            if current_evaluation is True:
                matched_files.append(current_file)
        return matched_files

    def __init__(self, path, query):
        self.current_compilation = []

        compile_start = datetime.datetime.now()
        self.compile(query)
        compile_end = datetime.datetime.now()

        parse_start = datetime.datetime.now()
        parsed_ast = self.parse(self.current_compilation)
        parse_end = datetime.datetime.now()

        # Execute search
        results_start = datetime.datetime.now()
        results = self.execute(parsed_ast)
        results_end = datetime.datetime.now()
        # Produce timing output
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

        # Produce results
        for result in results:
            print(result.path)

class Application(object):
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

        query = SearchQuery(filepath, query)

if __name__ == "__main__":
    Application().main()
