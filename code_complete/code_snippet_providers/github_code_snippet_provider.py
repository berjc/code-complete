# -*- coding: utf-8 -*-

""" Encapsulates Functionality for Gathering Relevant Code Snippets from Github. """

import httplib
from lxml import html
import requests

from abstract_code_snippet_provider import AbstractCodeSnippetProvider
from utils.request_builder import RequestBuilder


class GithubCodeSnippetProvider(AbstractCodeSnippetProvider):
    """ Encapsulates Functionality for Gathering Relevant Code Snippets from Github. """

    PATH_DELIM = '/'
    SPACE_DELIM = '+'

    # The number of search pages to iterate through on Github.
    NUM_PAGES_TO_CHECK = 2

    GITHUB_DOMAIN = 'github.com'
    GITHUB_SEARCH_PATH = '/search'

    RAW_GITHUB_USER_CONTENT_DOMAIN = 'raw.githubusercontent.com'
    BLOB_INDEX = 3

    # Github Search Request Parameters.
    GITHUB_LANGUAGE_KEY = 'l'
    GITHUB_QUERY_KEY = 'q'
    GITHUB_PAGE_KEY = 'p'
    GITHUB_TYPE_KEY = 'type'
    GITHUB_TYPE_VALUE = 'Code'

    # The xpath for parsing snippet URLs from the Github search results page.
    XPATH_SNIPPET_URLS = '//div[contains(@class, "code-list-item") and contains(@class, "code-list-item-public")]' \
        '//p[@class="title"]//a[@title]/@href'

    def __init__(self, task_description, language):
        """ Initializes the `GithubCodeSnippetProvider` object.

        :param task_description: A description of the task to complete.
        :type task_description: str
        :param language: The programming language the code snippets should be in.
        :type language: str
        """
        AbstractCodeSnippetProvider.__init__(self, task_description, language)

    @staticmethod
    def _construct_raw_user_content_url_path(code_snippet_url):
        """ Returns the raw user content URL for the given code snippet URL.

        :return: The raw user content URL for the given code snippet URL.
        :rtype: str

        .. code-block:: python

            code_snippet_url = '/username/reponame/blob/hashvalue/path/to/file'

            # Returns ...

                '/username/reponame/hashvalue/path/to/file'
        """
        parts_of_path = code_snippet_url.split(GithubCodeSnippetProvider.PATH_DELIM)
        return GithubCodeSnippetProvider.PATH_DELIM.join(
            parts_of_path[:GithubCodeSnippetProvider.BLOB_INDEX] +
            parts_of_path[GithubCodeSnippetProvider.BLOB_INDEX + 1:]
        )

    @staticmethod
    def _get_code_snippets_from_snippet_urls(code_snippet_urls):
        """ Returns the code snippets resident at the given snippet URls.

        :param code_snippet_urls: A list of the URLs of code snippets related to the given task description and
            language.
        :type code_snippet_urls: list

        :return: A list of the code snippets resident at the given snippet URLs.
        :rtype: list
        """
        code_snippets = []
        for code_snippet_url in code_snippet_urls:
            raw_user_content_url_path = GithubCodeSnippetProvider._construct_raw_user_content_url_path(code_snippet_url)
            request_url = RequestBuilder(
                GithubCodeSnippetProvider.RAW_GITHUB_USER_CONTENT_DOMAIN,
                path=raw_user_content_url_path,
            ).build()
            page = requests.get(request_url)
            code_snippets.append(page.content)
        return code_snippets

    def _get_code_snippet_urls(self):
        """ Returns the URLs of all code snippets related to the given task description and language.

        :return: A list of the URLs of code snippets related to the given task description and language.
        :rtype: list
        """
        code_snippet_urls = []
        for page_number in xrange(GithubCodeSnippetProvider.NUM_PAGES_TO_CHECK):
            request_url = RequestBuilder(
                GithubCodeSnippetProvider.GITHUB_DOMAIN,
                path=GithubCodeSnippetProvider.GITHUB_SEARCH_PATH,
                params={
                    GithubCodeSnippetProvider.GITHUB_LANGUAGE_KEY: self._language,
                    GithubCodeSnippetProvider.GITHUB_PAGE_KEY: page_number + 1,
                    GithubCodeSnippetProvider.GITHUB_QUERY_KEY: GithubCodeSnippetProvider.SPACE_DELIM.join(
                        self._task_description.split()
                    ),
                    GithubCodeSnippetProvider.GITHUB_TYPE_KEY: GithubCodeSnippetProvider.GITHUB_TYPE_VALUE,
                },
            ).build()
            page = requests.get(request_url)
            if page.status_code != httplib.OK:
                # This occurs if the page number exceeds the the number of pages for the available search results.
                break
            tree = html.fromstring(page.content)
            code_snippet_urls[0:0] = tree.xpath(GithubCodeSnippetProvider.XPATH_SNIPPET_URLS)
        return code_snippet_urls

    def get_code_snippets(self):
        """ Returns the code snippets related to the given task description and language.

        :return: A list of code snippets related to the given task description and language.
        :rtype: list
        """
        code_snippet_urls = self._get_code_snippet_urls()
        self._code_snippets = GithubCodeSnippetProvider._get_code_snippets_from_snippet_urls(code_snippet_urls)
        return self._code_snippets
