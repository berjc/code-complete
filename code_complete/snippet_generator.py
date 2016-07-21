# -*- coding: utf-8 -*-

"""  """

from config import LANGUAGE
from snippet_providers.github_snippet_provider import GithubSnippetProvider


class SnippetGenerator(object):
    """ Encapsulates Functionality for Generating Code Snippets for a Task Description.

    :attr _code_snippets: A list of code snippets represented as strings.
    :type _snippets: list
    :attr _snippet_providers: A list of `AbstractSnippetProviders` for gathering code snippets.
    :type _snippet_providers: list
    """
    SNIPPET_PROVIDERS = [
        GithubSnippetProvider,
    ]

    def __init__(self, task_description):
        """ Initializes the `SnippetGenerator` object.

        :param task_description: A description of the task to complete.
        :type task_description: str
        """
        self._snippets = []
        self._snippet_providers = [
            snippet_provider(task_description, LANGUAGE) for snippet_provider in SnippetGenerator.SNIPPET_PROVIDERS
        ]

    def generate_snippets(self):
        """ Generate snippets for the task description.

        :return: A list of code snippets represented as strings.
        :rtype: list
        """
        for snippet_provider in self._snippet_providers:
            self._snippets += snippet_provider.get_snippets()
        return self._snippets
