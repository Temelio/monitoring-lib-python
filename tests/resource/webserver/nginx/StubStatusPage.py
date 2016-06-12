# -*- coding: utf-8 -*-

"""
StubStatusPage class tests
--------------------------

Tests for `StubStatusPage` class.
"""


from nagiosplugin import Metric
import pytest
import requests_mock


from temelio_monitoring.resource.webserver.nginx import StubStatusPage


NGINX_STUB_STATUS_MOCK = """
Active connections: 291
server accepts handled requests
 16630948 16630948 31070465
Reading: 6 Writing: 179 Waiting: 106
"""

METRICS_DATA = [
    Metric('active_connections', 291, min=0, context='active_connections'),
    Metric('active_reading', 6, min=0, context='default'),
    Metric('active_waiting', 106, min=0, context='active_waiting'),
    Metric('active_writing', 179, min=0, context='default'),
    Metric('total_accept', 16630948, min=0, context='default'),
    Metric('total_connections', 31070465, min=0, context='default'),
    Metric('total_handled', 16630948, min=0, context='default'),
]

NGINX_STUB_STATUS_MOCK_INVALID = 'foobar'


def test_with_invalid_url():
    """
    Check if get_status_data() called without args
    """

    with pytest.raises(RuntimeError) as error:
        resource = StubStatusPage('')
        next(resource.probe())

    assert 'Invalid URL' in str(error.value)


def test_with_bad_nginx_response():
    """
    Check if get_status_data() called with bad Nginx response
    """

    with requests_mock.mock() as mock:
        mock.get('http://localhost/nginx_stats',
                 text=NGINX_STUB_STATUS_MOCK_INVALID)

        with pytest.raises(RuntimeError) as error:
            resource = StubStatusPage('http://localhost/nginx_stats')
            next(resource.probe())

        assert 'Output not correctly parsed !' in str(error.value)


def test_without_auth():
    """
    Check if get_status_data() called without authentication data
    """

    with requests_mock.mock() as mock:
        mock.get('http://localhost/nginx_stats', text=NGINX_STUB_STATUS_MOCK)
        contexts = ['active_connections', 'active_waiting']
        resource = StubStatusPage('http://localhost/nginx_stats',
                                  contexts=contexts)

        all_metrics = sorted(resource.probe())
        metric_index = 0

        for metric in all_metrics:
            assert metric.name == METRICS_DATA[metric_index].name
            assert metric.value == METRICS_DATA[metric_index].value
            assert metric.min == METRICS_DATA[metric_index].min
            assert metric.context == METRICS_DATA[metric_index].context
            metric_index += 1


def test_with_auth():
    """
    Check if get_status_data() called with authentication data
    """

    with requests_mock.mock() as mock:
        mock.get('http://localhost/nginx_stats', text=NGINX_STUB_STATUS_MOCK)
        contexts = ['active_connections', 'active_waiting']
        resource = StubStatusPage('http://localhost/nginx_stats',
                                  username='foo',
                                  password='bar',
                                  contexts=contexts)

        all_metrics = sorted(resource.probe())
        metric_index = 0

        for metric in all_metrics:
            assert metric.name == METRICS_DATA[metric_index].name
            assert metric.value == METRICS_DATA[metric_index].value
            assert metric.min == METRICS_DATA[metric_index].min
            assert metric.context == METRICS_DATA[metric_index].context
            metric_index += 1


def test_with_bad_auth():
    """
    Check if get_status_data() called without authentication data
    """

    with requests_mock.mock() as mock:
        mock.get('http://localhost/nginx_stats', text='foo', status_code=403)
        resource = StubStatusPage('http://localhost/nginx_stats')

        with pytest.raises(RuntimeError) as error:
            resource = StubStatusPage('http://localhost/nginx_stats')
            next(resource.probe())

        assert '403 : "foo"' in str(error.value)
