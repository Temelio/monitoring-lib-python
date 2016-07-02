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
        :param requests: 'metric_name;;json_path;;context_name' list
        :param request_separator: Reparator used in request string
        :type url: string
        :type username: string
        :type password: string
        :type requests: list
        :type request_separator: string
        """

        self.src = kwargs.get('src', '')
        self.username = kwargs.get('username', '')
        self.password = kwargs.get('password', '')
        self.certificate_file = kwargs.get('certificate_file', '')
        self.key_file = kwargs.get('key_file', '')
        self.requests = kwargs.get('requests', [])
        self.request_separator = kwargs.get('request_separator', ';;')

        if len(self.requests) == 0:
            raise CheckError('No request data to process')


    def _get_data_from_url(self):
        """
        Get status page content and return a dict with data

        :return: Request with JSON render
        :rtype: object
        """

        # Get status page content
        request = RequestsUtils.get(url=self.src,
                                    username=self.username,
                                    password=self.password,
                                    certificate_file=self.certificate_file,
                                    key_file=self.key_file)

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


    def _prepare_probe_requests(self):
        """
        Prepare JSON queries before probe processing

        :returns: tuples list (metric_name, json_path, context_name)
        :rtype: list
        """

        probe_requests = []

        for request_string in self.requests:

            # Split each query
            request = request_string.split(self.request_separator)
            if len(request) != 3:
                raise CheckError('Bad request format')

            # Metric name management
            if request[0] == '':
                request[0] = 'json-matches'

            # JSON path management
            try:
                request[1] = parse(request[1])
            except Exception as err:
                raise CheckError(RuntimeError(err))

            # Context name
            if request[2] == '':
                request[2] = request[0]

            probe_requests.append(tuple(request))

        return probe_requests


    def probe(self):
        """
        Get JSON data using JSON path and return Metric objects

        :return: a generator with data
        :rtype: generator
        """

        # Prepare check data before processing
        probe_requests = self._prepare_probe_requests()

        # Get data from src
        json_data = self._get_data()

        # Process each request
        for probe_request in probe_requests:

            # Get json_path target value
            matches = probe_request[1].find(json_data)

            # Build and return Metric objects from data
            yield Metric(probe_request[0],
                         matches,
                         context=probe_request[2])
