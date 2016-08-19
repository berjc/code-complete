# -*- coding: utf-8 -*-

""" Encapsulates Functionality for Testing and Iterating on the Code Complete File. """

import glob
import os
import re
import shutil
import subprocess

from config import READ_OPT
from config import WRITE_OPT


LINE = '=' * 100

# TODO : Fix Task Solution Comment
class CodeCompleter(object):
    """ Encapsulates Functionality for Testing and Iterating on the Code Completed File.

    :attr _current_code_f: The path to the current code completed version of the original code file.
    :type _current_code_f: str
    :attr _original_code_f: A path to the file to code complete.
    :type _original_code_f: str
    :attr _tests_f: A path to the tests to be used to verify code completion.
    :type _tests_f: str
    :attr _task_descriptors: A list of `TaskDescriptor` objects encapsulating the completion tasks.
    :type _task_descriptors: list
    :attr _task_solutions:
    :type _task_solutions: list
    """
    UNITTEST_OK = 'OK'
    UNITTEST_FAILURE_REGEX = r'\d+'

    PATH_DELIM = '/'
    COMMA_DELIM = ','
    EQUALS_DELIM = '='
    NEW_LINE_DELIM = '\n'

    ORIGINAL_EXTENSION = '%s.original'
    PREVIOUS_EXTENSION = '%s.previous'

    RUN_PYTHON_SCRIPT_CMD = 'python %s'
    ALL_PYC_FILES = '%s/*.pyc'

    APPEND_FUNCTION_STUB_TEMPLATE = '\n%s'
    FUNCTION_STUB_TEMPLATE = '%s%s(%s)'
    SET_VARIABLE_TEMPLATE = '%s %s '

    def __init__(self, code_f, tests_f, task_descriptors, task_solutions):
        """ Initializes the `CodeCompleter` object.

        :param code_f: A path to the file to code complete.
        :type code_f: str
        :param tests_f: A path to the tests to be used to verify code completion.
        :type tests_f: str
        :param task_descriptors: A list of `TaskDescriptor` objects encapsulating the completion tasks.
        :type task_descriptors: list
        :param task_solutions: ...
        :type task_solutions: list
        """
        self._current_code_f = code_f
        self._original_code_f = code_f
        self._tests_f = tests_f
        self._task_descriptors = task_descriptors
        self._task_solutions = task_solutions

    @staticmethod
    def _parse_unittest_results(results):
        """ Parses the number of test failures from `unittest.main()` output.

        Examples of the last line of the `unittest.main()` output.

        .. code-block:: python

            OK  # <-- Signals all tests passed.

            FAILED (failures=1)  # <-- Signals 1 test failed.
        """
        print results
        last_line = results.split(CodeCompleter.NEW_LINE_DELIM)[-1].strip()
        if last_line == CodeCompleter.UNITTEST_OK:
            return 0
        elif not last_line.startswith('FAILED'):
            return None
        else:
            return sum([
                int(count) for count in re.findall(CodeCompleter.UNITTEST_FAILURE_REGEX, last_line, re.M | re.I)
            ])

    def _remove_compiled_code(self):
        """ Removes compiled python files from the code file's location. """
        path_to_code_file = CodeCompleter.PATH_DELIM.join(self._current_code_f.split(CodeCompleter.PATH_DELIM)[:-1])
        for f in glob.glob(CodeCompleter.ALL_PYC_FILES % path_to_code_file):
            os.remove(f)

    def _run_tests(self):
        """ Returns the number of tests that failed.

        :return: The number of tests that failed.
        :rtype: int
        """
        process = subprocess.Popen(
            CodeCompleter.RUN_PYTHON_SCRIPT_CMD % self._tests_f,
            shell=True,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        return CodeCompleter._parse_unittest_results(stderr.strip())

    def _attempt_to_solve_task(self, task_descriptor, task_solution):
        """ Attempt to solve task with the given task descriptor using the given task solution.

        :param task_descriptor: The `TaskDescriptor` object to use to solve the task.
        :type task_descriptor: TaskDescriptor
        :param task_solution:
        :type task_solution:
        """
        stub_function, input_list, output_list, function_name = task_solution
        current_code_f_contents = open(self._current_code_f, READ_OPT).read()
        current_code_f_contents += CodeCompleter.APPEND_FUNCTION_STUB_TEMPLATE % stub_function
        current_code_f_contents = current_code_f_contents.replace(
            task_descriptor.get_task_id(),
            CodeCompleter.FUNCTION_STUB_TEMPLATE % (
                CodeCompleter.SET_VARIABLE_TEMPLATE % (
                    CodeCompleter.COMMA_DELIM.join(output_list),
                    CodeCompleter.EQUALS_DELIM,
                ) if output_list else '',
                function_name,
                CodeCompleter.COMMA_DELIM.join(input_list),
            ),
        )
        open(self._current_code_f, WRITE_OPT).write(current_code_f_contents)

    def complete(self):
        """ Complete all tasks. """
        print '%s\n\nStarting with Code... \n\n%s' % (LINE, open(self._current_code_f, READ_OPT).read().replace('\n', '\n\t'))
        # Make a copy of the original code file.
        shutil.copyfile(self._original_code_f, CodeCompleter.ORIGINAL_EXTENSION % self._original_code_f)
        num_of_tests_failed = self._run_tests()
        for task_descriptor, task_solutions in zip(self._task_descriptors, self._task_solutions):
            # Make a copy of the current code file so that we can revert to it if the test verification fails.
            shutil.copyfile(self._current_code_f, CodeCompleter.PREVIOUS_EXTENSION % self._current_code_f)
            for task_solution in task_solutions:
                self._attempt_to_solve_task(task_descriptor, task_solution)
                print '%s\n\nTrying to Reduce %d Errors with...\n\n\t%s' % (
                    LINE,
                    num_of_tests_failed,
                    open(self._current_code_f, READ_OPT).read().replace('\n', '\n\t'),
                )
                raw_input()
                self._remove_compiled_code()
                updated_num_tests_failed = self._run_tests()
                if updated_num_tests_failed is None:
                    updated_num_tests_failed = num_of_tests_failed
                if updated_num_tests_failed < num_of_tests_failed:
                    num_of_tests_failed = updated_num_tests_failed
                    break
                else:
                    shutil.copyfile(CodeCompleter.PREVIOUS_EXTENSION % self._current_code_f, self._current_code_f)
        os.remove(CodeCompleter.PREVIOUS_EXTENSION % self._current_code_f)
        print '%s\n\nFINISHED with %d Errors!!! %s\n\n%s' % (LINE, num_of_tests_failed, ':(' if num_of_tests_failed else ':)', LINE)
