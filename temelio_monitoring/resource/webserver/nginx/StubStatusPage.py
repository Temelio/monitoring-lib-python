"""
This module manage the StubStatusPage class

This is an Nginx status page were we can see useful informations about
connections states count
"""


import re
from nagiosplugin import CheckError
from nagiosplugin import Metric
from nagiosplugin import Resource
from requests import get
from requests import RequestException


class StubStatusPage(Resource):
    """
    This ressource manage data in Nginx stub status page
    """

    def __init__(self, url='', username='', password='', contexts=None):
        """
        Initialize ressource attributes

        :param url: Nginx stub status url
        :param username: Username authorized to view stats
        :param password: Password of username authorized to view stats
        :param contexts: Managed contexts for probe metrics
        :type url: string
        :type username: string
        :type password: string
        :type contexts: list
        """

        self.url = url
        self.username = username
        self.password = password
        self.contexts = []

        if isinstance(contexts, list):
            self.contexts = contexts


    def _get_metric_context(self, metric_name):
        """
        Get applicable context for a metric

        :param metric_name: Metric name
        :type metric_name: string
        """

        if metric_name in self.contexts:
            return metric_name

        return 'default'


    def _get_status_data(self):
        """
        Get status page content and return a dict with data

        :return: Nginx status data
        :rtype: list
        """

        data_regex = r"""
            ^[a-z\s]+:\s*
            (?P<active_connections>\d+)\s*
            [a-z\s]+
            (?P<total_accept>\d+)\s+
            (?P<total_handled>\d+)\s+
            (?P<total_connections>\d+)\s+
            reading:\s*(?P<active_reading>\d+)\s*
            writing:\s*(?P<active_writing>\d+)\s*
            waiting:\s*(?P<active_waiting>\d+)\s*$"""

        regex = re.compile(data_regex,
                           re.VERBOSE | re.IGNORECASE | re.MULTILINE)

        # Get status page content
        try:
            request = get(self.url, auth=(self.username, self.password))
        except RequestException as err:
            raise CheckError(RuntimeError(err))

        # Parse status code
        if request.status_code >= 400:
            raise CheckError(RuntimeError('%i : "%s"' % (request.status_code,
                                                         request.text)))

        # Parse status page content
        matches = regex.match(request.text)
        if not matches:
            raise CheckError(RuntimeError('Output not correctly parsed !'))

        # Return stats into a dict
        return matches.groupdict()


    def probe(self):
        """
        Get status page content and return Metric objects

        :return: a generator with statistics
        :rtype: generator
        """

        # Get statistics
        nginx_stats = self._get_status_data()

        # Build and return Metric objects from data
        for key in nginx_stats:
            context = self._get_metric_context(key)

            yield Metric("%s" % key,
                         int(nginx_stats[key]),
                         min=0,
                         context=context)
