# -*- coding: utf-8 -*-

""" Encapsulates Functionality for Testing and Iterating on the Code Complete File. """

import glob
import os
import re
import shutil
import subprocess


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
    :attr _task_solutions: ...
    :type _task_solutions: list
    """
    READ_OPT = 'r'
    WRITE_OPT = 'w'

    UNITTEST_OK = 'OK'
    UNITTEST_FAILURE_REGEX = r'FAILED \((.*)=(.*)\)'
    UNITTEST_FAILURE_REGEX_GROUP_INDEX = 2

    PATH_DELIM = '/'
    COMMA_DELIM = ','
    OUTER_PAREN = ')'
    EQUALS_DELIM = '='
    NEW_LINE_DELIM = '\n'

    ORIGINAL_EXTENSION = '%s.original'
    PREVIOUS_EXTENSION = '%s.previous'

    CMD_LINE_PYTHON = 'python %s'
    PYC_FILES = '%s/*.pyc'

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
    def _parse_test_results(results):
        """ Parses the number of tests failures from `unittest` output.

        Examples of the last line of the `unittest.main()` output.

        .. code-block:: python

            OK  # <-- Signals all tests passed.

            FAILED (failures=1)  # <-- Signals 1 test failed.
        """
        last_line = results.split(CodeCompleter.NEW_LINE_DELIM)[-1].strip()
        if last_line == CodeCompleter.UNITTEST_OK:
            return 0
        else:
            return int(
                re.search(
                    CodeCompleter.UNITTEST_FAILURE_REGEX,
                    last_line,
                    re.M | re.I,
                ).group(CodeCompleter.UNITTEST_FAILURE_REGEX_GROUP_INDEX)
            )

    def _remove_compiled_code(self):
        """ Removes compiled python files from code file's location. """
        path_to_code_file = CodeCompleter.PATH_DELIM.join(self._current_code_f.split(CodeCompleter.PATH_DELIM)[:-1])
        for f in glob.glob(CodeCompleter.PYC_FILES % path_to_code_file):
            os.remove(f)

    def _run_tests(self):
        """ Returns the number of tests that failed.

        :return: The number of tests that failed.
        :rtype: int
        """
        process = subprocess.Popen(CodeCompleter.CMD_LINE_PYTHON % self._tests_f, shell=True, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return CodeCompleter._parse_test_results(stderr.strip())

    def _attempt_to_solve_task(self, task_descriptor, task_solution):
        """ Attempt to solve task with the given task descriptor using the given task solution.

        :param task_descriptor: The `TaskDescriptor` object to use to solve the task.
        :type task_descriptor: TaskDescriptor
        :param task_solution:
        :type task_solution:
        """
        # TODO : Fix `task_solution` comment.
        stub_function, input_list, output_list, function_name = task_solution
        current_code_f_contents = open(self._current_code_f, CodeCompleter.READ_OPT).read()
        current_code_f_contents += '%s%s' % (CodeCompleter.NEW_LINE_DELIM, stub_function)
        current_code_f_contents = current_code_f_contents.replace(
            task_descriptor.get_task_id(),
            '%s%s(%s)' % (
                '%s %s ' % (
                    CodeCompleter.COMMA_DELIM.join(output_list),
                    CodeCompleter.EQUALS_DELIM,
                ) if output_list else '',
                function_name,
                CodeCompleter.COMMA_DELIM.join(input_list),
            ),
        )
        open(self._current_code_f, CodeCompleter.WRITE_OPT).write(current_code_f_contents)

    def complete(self):
        """ Complete all tasks. """
        # Make a copy of the original code file.
        shutil.copyfile(self._original_code_f, CodeCompleter.ORIGINAL_EXTENSION % self._original_code_f)
        num_of_tests_failed = self._run_tests()
        for task_descriptor, task_solutions in zip(self._task_descriptors, self._task_solutions):
            # Make a copy of the current code file.
            shutil.copyfile(self._current_code_f, CodeCompleter.PREVIOUS_EXTENSION % self._current_code_f)
            for task_solution in task_solutions:
                self._attempt_to_solve_task(task_descriptor, task_solution)
                self._remove_compiled_code()
                updated_num_tests_failed = self._run_tests()
                if updated_num_tests_failed < num_of_tests_failed:
                    num_of_tests_failed = updated_num_tests_failed
                    break
                else:
                    shutil.copyfile(CodeCompleter.PREVIOUS_EXTENSION % self._current_code_f, self._current_code_f)
