# -*- coding: utf-8 -*-

""" Encapsulates Functionality for Generating Code Snippets for a Task Description. """

from config import LANGUAGE
from code_snippet_providers.github_code_snippet_provider import GithubCodeSnippetProvider


class CodeSnippetGenerator(object):
    """ Encapsulates Functionality for Generating Code Snippets for a Task Description.

    :attr _code_snippets: A list of code snippets represented as strings.
    :type _code_snippets: list
    :attr _code_snippet_providers: A list of `AbstractCodeSnippetProviders` for gathering code snippets.
    :type _code_snippet_providers: list
    """
    CODE_SNIPPET_PROVIDERS = [
        GithubCodeSnippetProvider,
    ]

    def __init__(self, task_description):
        """ Initializes the `CodeSnippetGenerator` object.

        :param task_description: A description of the task to complete.
        :type task_description: str
        """
        self._code_snippets = []
        self._code_snippet_providers = []
        for code_snippet_provider in CodeSnippetGenerator.CODE_SNIPPET_PROVIDERS:
            self._code_snippet_providers.append(code_snippet_provider(task_description, LANGUAGE))

    def generate_code_snippets(self):
        """ Generates and returns code snippets for the task description.

        :return: A list of code snippets represented as strings.
        :rtype: list
        """
        for code_snippet_provider in self._code_snippet_providers:
            self._code_snippets += code_snippet_provider.get_code_snippets()
        return self._code_snippets
