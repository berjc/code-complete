# -*- coding: utf-8 -*-

""" Encapsulates the CodeComplete Compiler. """

import importlib
import inspect
import itertools
import optparse
import os
import types
from snippet_analysis.snippet_controller import SnippetController

from code_completer import CodeCompleter
from code_snippet_generator import CodeSnippetGenerator
from config import READ_OPT
from config import TASK_INDICATOR
from task_descriptor import TaskDescriptor


class TaskSolutionGenerator(object):

    def __init__(self, task_descriptors, code_snippets_for_task_descriptors):
        self._task_solutions = []
        self._task_descriptors = task_descriptors
        self._code_snippets = code_snippets_for_task_descriptors

    def get_task_solutions(self):
        for task_descriptor, code_snippets in zip(self._task_descriptors, self._code_snippets):
            task_solutions = []
            for code_snippet in code_snippets:
                snippet_controller = SnippetController(code_snippet, task_descriptor.get_task_input_info(),
                                                       task_descriptor.get_task_description())
                match_functions, detail_functions = snippet_controller.find_snippet()

                for function in match_functions:
                    for combination in detail_functions[function][2]:
                        task_solutions.append([''.join(detail_functions[function][0][0]),
                                            [x[0] for x in combination],
                                            task_descriptor.get_task_output_info().keys(),
                                            function])
            self._task_solutions.append(task_solutions)
        return self._task_solutions


class Compiler(object):
    """ Encapsulates Functionality Necessary for Compiling a File to Code Completion.

    :attr _code_f: A path to the file to code complete.
    :type _code_f: str
    :attr _tests_f: A path to the tests to be used to verify code completion.
    :type _tests_f: str
    """
    def __init__(self, code_f, tests_f):
        """ Initializes the `Compiler` object.

        :param code_f: A path to the file to code complete.
        :type code_f: str
        :param tests_f: A path to the tests to be used to verify code completion.
        :type tests_f: str
        """
        self._code_f = code_f
        self._tests_f = tests_f

    @staticmethod
    def _get_code_snippets_for_task_descriptors(task_descriptors):
        """ Returns the code snippets found by the `CodeSnippetGenerator` for each task descriptor.

        :param task_descriptors: A list of `TaskDescriptor` objects encapsulating the completion tasks.
        :type: list

        :return: The code snippets found by the `CodeSnippetGenerator` for each task descriptor.
        :rtype: list
        """
        code_snippets = []
        for task_descriptor in task_descriptors:
            code_snippets.append(CodeSnippetGenerator(task_descriptor.get_task_description()).generate_code_snippets())
        return code_snippets

    def _extract_tasks_from_code(self):
        """ Extract tasks from code file.

        :return: A list of `TaskDescriptor` objects encapsulating the completion tasks found in the code file.
        :rtype: list
        """
        task_descriptors = []
        with open(self._code_f, READ_OPT) as code_f:
            for line in code_f:
                cleaned_line = line.strip()
                if cleaned_line.startswith(TASK_INDICATOR):
                    task_descriptors.append(TaskDescriptor(cleaned_line))
        return task_descriptors

    def compile(self):
        """ Compiles code file to code completion using tests as verification. """
        task_descriptors = self._extract_tasks_from_code()
        code_snippets_for_task_descriptors = self._get_code_snippets_for_task_descriptors(task_descriptors)
        task_solutions = TaskSolutionGenerator(
            task_descriptors,
            code_snippets_for_task_descriptors,
        ).get_task_solutions()
        CodeCompleter(self._code_f, self._tests_f, task_descriptors, task_solutions).complete()


# Setup the Command-Line Option Parser.
parser = optparse.OptionParser()
parser.add_option('-c', '--code', dest='code_f', help='code complete FILE', metavar='FILE')
parser.add_option('-t', '--tests', dest='test_f', help='run FILE to verify code completion', metavar='FILE')


if __name__ == '__main__':
    (options, args) = parser.parse_args()

    if not options.code_f:
        parser.error('File to code complete not provided.')
    elif not os.path.exists(options.code_f):
        parser.error('File at `%s` does not exist.' % options.code_f)

    if not options.test_f:
        parser.error('Tests not provided.')
    elif not os.path.exists(options.test_f):
        parser.error('File at `%s` does not exist.' % options.test_f)

    Compiler(options.code_f, options.test_f).compile()
