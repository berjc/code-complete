import sys
import os
from cStringIO import StringIO
from enum import Enum


class LanguageMode(Enum):
    python = 0
    shell = 1


class SnippetAnalysisHelper:
    """ Helper class to Snippet Analysis. Holds helper methods and list of language tokens.

    This class takes in a language mode, and generates language-specific tokens to take into account during analysis.
    It also contains static helper methods to help in the analysis.

    :param language_mode: A LanguageMode enum object declaring the language to be analyzed
    """

    def __init__(self, language_mode=LanguageMode.python):
        self.word_operator = "operator"
        self.word_unknown = "unknown"
        self.word_wildcard = "wildcard"
        self.language_mode = language_mode
        self.unique_identifier = "redirected_output_hiw_unique"
        self.filename = "code_complete_temp_file.py"

        if language_mode == LanguageMode.python:
            self.operators = ['+', '-', '/', '*', '(', ')', '[', ']', '{', '}', ',']
            self.unneeded_tokens = [':']
            self.scope_indicators = ['def']
            self.scope_break_indicators = ['return']
            self.ignore_flags = ['print', 'raw_input']
            self.ignore_classes = ['function']

    def exec_wrapper(self, code_to_execute):
        """ This static method takes in a string, which is a valid code snippet. The code is then run and the output of
        the run is returned

        :param code_to_execute: A String that wraps valid a valid code snippet
        :type str

        :return The output of the code_to_execute after it has run
        :rtype str
        """
        old_stdout = sys.stdout
        redirected_output_hiw_unique = sys.stdout = StringIO()

        if self.language_mode == LanguageMode.shell:
            os.popen(code_to_execute)

        elif self.language_mode == LanguageMode.python:
            exec code_to_execute

        sys.stdout = old_stdout
        self.reset_stdout()
        return redirected_output_hiw_unique.getvalue()

    @staticmethod
    def reset_stdout():
        """ This static method resets  system stdout to the default stdout
        """
        sys.stdout = sys.__stdout__

    @staticmethod
    def clean_type(type_to_clean):
        """ This static method takes in a String of the format "<type 'x'>" and trims it to return only x.

        :param type_to_clean: A string of format <type 'some_string'>"
        :type str

        :return The trimmed string
        :rtype str
        """
        new_type = type_to_clean[type_to_clean.find(" '"):type_to_clean.find(">")]
        return new_type.replace(' ', '').replace("'", "")

    def clean_dict(self, type_dict):
        """ This method takes in a Dictionary and removes keys of zero length and keys of operational or unknown
        types. Ideally, these removed keys are not required for the type analysis of variables.

        :param type_dict: A dictionary
        :type dict

        :return The trimmed dictionary
        :rtype dict
        """
        new_type_dict = {}
        for key, value in type_dict.iteritems():
            if not len(key) or value == self.word_unknown or value == self.word_operator:
                continue
            try:
                int(key)
            except:
                new_type_dict[key] = value

        return new_type_dict

    def get_local_scope_finder(self, spaces):
        """ This method returns the language specific methods for finding local variables in scope

        :param spaces: If the language is anal about indentation, spaces tell how much to indent
        :type str

        :return Code stub
        :rtype str
        """
        if self.language_mode == LanguageMode.python:
            return "\n" + spaces + "print locals()\n"

    def get_type_finder(self, word, spaces):
        """ This method returns the language specific methods for finding type of a method

        :param word: The word whose type is to be found
        :type str

        :param spaces: If the language is anal about indentation, spaces tell how much to indent
        :type str

        :return Code stub
        :rtype str
        """
        if self.language_mode == LanguageMode.python:
            return "\n" + spaces + "print type(" + word + ")\n"

    def is_global(self, output):
        """ This method returns if the output is from global scope or not. This is done by comparing against the
        variable name in function exec_wrapper

        :param output: The output of an exec
        :type str

        :rtype bool
        """
        return output.find(self.unique_identifier) >= 0
