# -*- coding: utf-8 -*-

""" `TaskDescriptor` Encapsulates Information Relating to a CodeCompletion Task. """

from config import TASK_DELIM
from config import TASK_INDICATOR


class TaskDescriptor(object):
    """ Encapsulates Information Relating to a CodeCompletion Task.

    :attr _task_description: A description of the task to complete.
    :type _task_description: str
    :attr _task_args_info: A mapping of the inputs of the task and to the types of those inputs.
    :type _task_args_info: dict
    """
    def __init__(self, comment):
        """ Initialize `TaskDescriptor` by extracting task information from the given task comment.

        :param comment: A comment containing task information.
        :type comment: str
        """
        self._task_description, self._task_args_info = TaskDescriptor._extract_task_info(comment)

    @staticmethod
    def _extract_task_info(comment):
        """ Extract task information from task comment.

        :param comment: A comment containing task information.
        :type comment: str

        :return: A 2-Tuple containing the task description and the task's argument information.
        :rtype: tuple

        Example of a task comment:

        .. code-block:: python

            ### sort a list of strings in alphabetical order ::: [('my_list', 'list')]

            # Returns ...

                ('sort a list of strings in alphabetical order', {'my_list' : 'list'})
        """
        unclean_task_description, task_args_info_string = comment.lstrip(TASK_INDICATOR).split(TASK_DELIM)
        return unclean_task_description.strip(), dict(eval(task_args_info_string))
