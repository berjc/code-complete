# -*- coding: utf-8 -*-

""" Encapsulates Functionality for Building Web Requests. """


class RequestBuilder(object):
    """ Encapsulates Functionality for Building Web Requests.

    :attr _domain: The domain component of the request.
    :type _domain: str
    :attr _path: The path component of the request (default: '').
    :type _path: str
    :attr _scheme: The scheme component of the request (default: 'https').
    :type _scheme: str
    :attr _params: The parameters of the request (default: {}).
    :type _params: dict
    """
    DEFAULT_PATH = ''
    DEFAULT_SCHEME = 'https'

    QUERY_DELIM = '?'
    QUERY_KEY_VALUE_DELIM = '&'
    QUERY_KEY_VALUE_TEMPLATE = '%s=%s'

    URL_TEMPLATE = '%s://%s%s%s'

    def __init__(self, domain, path=None, scheme=None, params=None):
        """ Initializes the `RequestBuilder` object.

        :param domain: The domain component of the request.
        :type domain: str
        :param path: The path component of the request (default: None).
        :type path: str
        :param scheme: The scheme component of the request (default: None).
        :type scheme: str
        :param params: The parameters of the request (default: None).
        :type params: dict
        """
        self._domain = domain
        self._path = path or RequestBuilder.DEFAULT_PATH
        self._scheme = scheme or RequestBuilder.DEFAULT_SCHEME
        self._params = params or {}

    def build(self):
        """ Returns the request as a well-formed URL.

        :return: The request as a well-formed URL.'
        :rtype: str
        """
        params_string = RequestBuilder.QUERY_DELIM if self._params else ''
        params_string += RequestBuilder.QUERY_KEY_VALUE_DELIM.join([
            RequestBuilder.QUERY_KEY_VALUE_TEMPLATE % (key, str(value)) for key, value in self._params.iteritems()
        ])
        return RequestBuilder.URL_TEMPLATE % (self._scheme, self._domain, self._path, params_string)
