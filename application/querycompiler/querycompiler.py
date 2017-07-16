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

import parse
import tokens
import errors

from searchquery import SearchQuery

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
"""
    A list of tokens that the lexer will recognize and in what order to look for them.
"""

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

class QueryCompiler(object):
    """
        The query compiler class. This class is used to compile string queries into executable
        SearchQuery objects.
    """

    current_compilation = None
    """
        The current compilation result.
    """

    previous_token = None
    """
        The previous token that was processed.
    """

    logic_stack = None
    """
        A list of list references that contains where in the logic stack we are.
    """

    timed = False
    """
        Whether or not the search should be timed. This is a debugging tool.
    """

    compiled_data = None
    """
        The compiled query data from the compiler.
    """

    def handle_timed_flag(self):
        self.timed = True

    def handle_verbose_flag(self):
        pass

    FLAG_HANDLERS = {
        "timed": handle_timed_flag,
        "verbose": handle_verbose_flag,
    }

    def handle_flags_token(self, index, token, token_stream, query):
        flags = token.match_data.group(1).split(",")

        # Must be the first index
        if index != 0:
            raise errors.SyntaxError(expected=[])

        called_functions = []
        for current_flag in flags:
            current_flag = current_flag.lower()

            if current_flag not in self.FLAG_HANDLERS:
                raise errors.SyntaxError(expected=[])
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
            raise errors.BadParenthesesError()
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

    def compile(self, query, optimized=True):
        """
            Compiles the input query into a SearchQuery object.
        """

        self._lex(query)
        result = SearchQuery(compiled_data=self._parse(self.current_compilation))
        print(result.compiled_data)
        if optimized:
            result.optimize()
        return result

    def _lex(self, query):
        """
            The initial stage of compilation. We lex the input query into a format that is easier for the
            parser to deal with.
        """

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
                        raise errors.SyntaxError(expected=expected_tokens, query=query, previous_token=self.previous_token, found=current_token, token_index=current_index)

                self.previous_token = current_token
                current_stream = self.TOKEN_HANDLERS[current_token_type](self, current_index, current_token, token_stream, query)
                current_index += 1
        except StopIteration as e:
            pass

        if len(self.logic_stack) != 1:
            raise errors.BadParenthesesError()
        return

    def _parse(self, compiled_data):
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

        # Second pass: Convert sub queries
        produced_ast = [current_element if type(current_element) is not list else SearchQuery(self._parse(current_element)) for current_element in produced_ast]

        # Third pass: Match data to their operators
        removed_entries = []
        for index, current_element in enumerate(produced_ast):
            current_element_type = type(current_element)

            if current_element_type in parse.operators.Operator.__subclasses__():
                current_element.lhs = produced_ast[index - 1]
                current_element.rhs = produced_ast[index + 1]
                removed_entries.append(current_element.lhs)
                removed_entries.append(current_element.rhs)

        produced_ast = [current_element for current_element in produced_ast if current_element not in removed_entries]

        # Fourth pass: Match logical operands
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
