"""
This module manage the GetValueByStringPath class

Get a value from a JSON document using a string JSON path
"""


from nagiosplugin import CheckError
from nagiosplugin import Metric
from nagiosplugin import Resource
from jsonpath_rw import parse

from temelio_monitoring.utils import RequestsUtils


class GetValueByJsonPath(Resource):
    """
    This ressource manage value check from JSON string path
    """

    def __init__(self, **kwargs):
        """
        Initialize ressource attributes

        :param src: JSON target
        :param username: Username authorized to view JSON
        :param password: Password of username authorized to view JSON
        :param json_path: JSON path used to get value
        :param metric_name: Metric name returned with this search
        :param context_name: Context name to set for this metric
        :type url: string
        :type username: string
        :type password: string
        :type json_path: string
        :type metric_name: string
        :type context_name: string
        """

        self.src = kwargs.get('src', '')
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')
        self.metric_name = kwargs.get('metric_name', 'json-matches')
        self.context_name = kwargs.get('context_name', self.metric_name)

        try:
            self.json_path = parse(kwargs.get('json_path', ''))
        except Exception as err:
            raise CheckError(RuntimeError(err))


    def _get_data_from_url(self):
        """
        Get status page content and return a dict with data

        :return: Request with JSON render
        :rtype: object
        """

        # Get status page content
        request = RequestsUtils.get(url=self.src,
                                    username=self.username,
                                    password=self.password)

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
        Get JSON data using JSON path and return Metric objects

        :return: a generator with data
        :rtype: generator
        """

        # Get data from src
        json_data = self._get_data()

        # Get json_path target value
        matches = self.json_path.find(json_data)

        # Build and return Metric objects from data
        return Metric(self.metric_name,
                      matches,
                      context=self.context_name)
