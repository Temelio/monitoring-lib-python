"""
This module manage the GetValueByStringPath class

Get a value from a JSON document using a string JSON path
"""


from nagiosplugin import CheckError
from nagiosplugin import Metric
from nagiosplugin import Resource
from jsonpath_rw import parse
from requests import get, RequestException


class GetValueByJsonPath(Resource):
    """
    This ressource manage value check from JSON string path
    """

    def __init__(self, src='', username='', password='',
                 json_path=''):
        """
        Initialize ressource attributes

        :param url: Nginx stub status url
        :param username: Username authorized to view stats
        :param password: Password of username authorized to view stats
        :param json_path: JSON path used to get value
        :type url: string
        :type username: string
        :type password: string
        :type json_path: string
        """

        self.src = src
        self.username = username
        self.password = password

        try:
            self.json_path = parse(json_path)
        except Exception as err:
            raise CheckError(RuntimeError(err))


    def _get_data_from_url(self):
        """
        Get status page content and return a dict with data

        :return: Request with JSON render
        :rtype: object
        """

        # Get status page content
        try:
            request = get(self.src, auth=(self.username, self.password))
        except RequestException as err:
            raise CheckError(RuntimeError(err))

        # Parse status code
        if request.status_code >= 400:
            raise CheckError(RuntimeError('%i : "%s"' % (request.status_code,
                                                         request.text)))
        return request.json()


    def _get_data(self):
        """
        Get JSON data from src.

        Only http is managed today.

        :return object: JSON data
        :rtype: object
        """

        # Get JSON data from URL
        return self._get_data_from_url()


    def probe(self):
        """
        Get status page content and return Metric objects

        :return: a generator with statistics
        :rtype: generator
        """

        # Get data from src
        json_data = self._get_data()

        # Get json_path target value
        matches = self.json_path.find(json_data)

        # Build and return Metric objects from data
        return Metric('json_matches',
                      matches,
                      context='json_value')
