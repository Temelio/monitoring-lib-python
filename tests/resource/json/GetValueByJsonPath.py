# -*- coding: utf-8 -*-

"""
GetValueByJsonPath class tests
------------------------------

Tests for `GetValueByJsonPath` class.
"""


from nagiosplugin import CheckError, Metric
import pytest
import requests_mock


from temelio_monitoring.resource.json import GetValueByJsonPath


def test_without_data():
    """
    Check if get_status_data() called without args
    """

    with pytest.raises(CheckError) as error:
        GetValueByJsonPath()

    assert "'NoneType' object has no attribute 'lineno'" in str(error.value)


def test_with_invalid_url():
    """
    Check if get_status_data() called without args
    """

    with pytest.raises(CheckError) as error:
        resource = GetValueByJsonPath(json_path='foo')
        resource.probe()

    assert 'Invalid URL' in str(error.value)


def test_with_bad_server_response():
    """
    Check if webserver return an error
    """

    with requests_mock.mock() as mock:

        fake_url = 'http://localhost/foo'
        mock.get(fake_url, status_code=500, text='Server error')

        with pytest.raises(CheckError) as error:
            resource = GetValueByJsonPath(json_path='foo', src=fake_url)
            next(resource.probe())

        assert '500 : "Server error"' in str(error.value)


def test_without_path_data():
    """
    Check if JSON path not exists
    """

    with requests_mock.mock() as mock:

        fake_url = 'http://localhost/foo'
        mock.get(fake_url, text='{"foobar": "foo"}')

        resource = GetValueByJsonPath(json_path='foo', src=fake_url)
        metric = resource.probe()

        assert isinstance(metric, Metric) is True
        assert len(metric.value) == 0


def test_with_path_data():
    """
    Check if JSON path exists
    """

    with requests_mock.mock() as mock:

        fake_url = 'http://localhost/foo'
        mock.get(fake_url, text='{"foo": "bar"}')

        resource = GetValueByJsonPath(json_path='foo', src=fake_url)
        metric = resource.probe()

        assert isinstance(metric, Metric) is True
        assert len(metric.value) == 1


@pytest.mark.parametrize('metric_name,expected_metric', [
    (None, 'json-matches'),
    ('foo', 'foo')
])
def test_default_metric_name(metric_name, expected_metric):
    """
    Check metric_name management
    """

    with requests_mock.mock() as mock:

        fake_url = 'http://localhost/foo'
        mock.get(fake_url, text='{"foo": "bar"}')

        if metric_name is None:
            resource = GetValueByJsonPath(json_path='foo', src=fake_url)
        else:
            resource = GetValueByJsonPath(json_path='foo',
                                          src=fake_url,
                                          metric_name=metric_name)
        metric = resource.probe()

        assert isinstance(metric, Metric) is True
        assert len(metric.value) == 1
        assert metric.name == expected_metric


@pytest.mark.parametrize('context_name,expected_context', [
    (None, 'json-matches'),
    ('foo', 'foo')
])
def test_default_context_name(context_name, expected_context):
    """
    Check context name management
    """

    with requests_mock.mock() as mock:

        fake_url = 'http://localhost/foo'
        mock.get(fake_url, text='{"foo": "bar"}')

        if context_name is None:
            resource = GetValueByJsonPath(json_path='foo', src=fake_url)
        else:
            resource = GetValueByJsonPath(json_path='foo',
                                          src=fake_url,
                                          context_name=context_name)
        metric = resource.probe()

        assert isinstance(metric, Metric) is True
        assert len(metric.value) == 1
        assert metric.context == expected_context
