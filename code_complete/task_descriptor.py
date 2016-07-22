# -*- coding: utf-8 -*-

""" Encapsulates Information Relating to a Code Completion Task. """

from config import TASK_DELIM
from config import TASK_INDICATOR


class TaskDescriptor(object):
    """ Encapsulates Information Relating to a Code Completion Task.

    :attr _task_id: The comment containing the code completion task.
    :attr _task_id: str
    :attr _task_description: A description of the task to complete.
    :type _task_description: str
    :attr _task_input_info: A mapping of the inputs of the task and to the types of those inputs.
    :type _task_input_info: dict
    :attr _task_output_info: A mapping of the outputs of the task and to the types of those outputs.
    :type _task_output_info: dict
    """
    def __init__(self, comment):
        """ Initialize `TaskDescriptor` by extracting task information from the given task comment.

        :param comment: A comment containing task information.
        :type comment: str
        """
        self._task_id = comment
        self._task_description, self._task_input_info, self._task_output_info \
            = TaskDescriptor._extract_task_info(comment)

    @staticmethod
    def _extract_task_info(comment):
        """ Extract task information from task comment.

        :param comment: A comment containing task information.
        :type comment: str

        :return: A 3-Tuple containing the task description, task input information, and task output information.
        :rtype: tuple

        Example of a task comment:

        .. code-block:: python

            ### sort a list of strings in alphabetical order ::: [('my_list', 'list')] ::: [('new_list', 'list')]

            # Returns ...

                ('sort a list of strings in alphabetical order', {'my_list' : 'list'}, {'new_list', 'list'})
        """
        unclean_task_description, task_input_info, task_output_info = comment.lstrip(TASK_INDICATOR).split(TASK_DELIM)
        return unclean_task_description.strip(), dict(eval(task_input_info)), dict(eval(task_output_info))

    def get_task_id(self):
        """ Returns the task ID for the task descriptor.

        :return: The task ID for the task descriptor.
        :rtype: str
        """
        return self._task_id

    def get_task_description(self):
        """ Returns the task description for the task descriptor.

        :return: The task description for the task descriptor.
        :rtype: str
        """
        return self._task_description

    def get_task_input_info(self):
        """ Returns the task's input information for the task descriptor.

        :return: The task's input information for the task descriptor.
        :rtype: dict
        """
        return self._task_input_info

    def get_task_output_info(self):
        """ Returns the task's output information for the task descriptor.

        :return: The task's output information for the task descriptor.
        :rtype: dict
        """
        return self._task_output_info
