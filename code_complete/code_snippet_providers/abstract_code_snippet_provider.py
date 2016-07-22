# -*- coding: utf-8 -*-

""" Encapsulates the Base API for Snippet Providers. """


class AbstractCodeSnippetProvider(object):
    """ A Template Class for Snippet Providers.

    :attr _snippets: A list of code snippets represented as strings.
    :type _code_snippets: list
    :attr _task_description: A description of the task to complete.
    :type _task_description: str
    :attr _language: The programming language the code snippets should be in.
    :type _language: str
    """
    def __init__(self, task_description, language):
        """ Initializes the `AbstractCodeSnippetProvider` object.

        :param task_description: A description of the task to complete.
        :type task_description: str
        :param language: The programming language the code snippets should be in.
        :type language: str
        """
        self._code_snippets = []
        self._task_description = task_description
        self._language = language

    def get_code_snippets(self):
        """ Returns the code snippets related to the given task description and language. """
        raise NotImplementedError
