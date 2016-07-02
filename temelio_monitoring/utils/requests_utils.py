"""
This module manage utils functions for requests module
"""

from nagiosplugin import CheckError
from requests import get, RequestException


class RequestsUtils(object):
    """
    This is the utils class for request module
    """

    @staticmethod
    def get(url='', username='', password='',
            certificate_file='', key_file=''):
        """
        Do a get request, with error management

        :param url: target URL
        :param username: Username authorized to view stats
        :param password: Password of username authorized to view stats
        :type url: string
        :type username: string
        :type password: string
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        try:
            request = get(url, auth=(username, password),
                          cert=(certificate_file, key_file))
        except RequestException as err:
            raise CheckError(RuntimeError(err))

        # Parse status code
        if request.status_code >= 400:
            raise CheckError(RuntimeError('%i : "%s"' % (request.status_code,
                                                         request.text)))

        return request
