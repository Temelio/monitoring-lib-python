# -*- coding: utf-8 -*-

"""
ScalarInfoValue class tests
---------------------------

Tests for `ScalarInfoValue` class.
"""

from nagiosplugin import Metric
import pytest

from temelio_monitoring.resource.database.redis import ScalarInfoValue


REDIS_INFO_MOCK = {
    'foo': 'bar',
    'foobar_int': 1,
    'foobar_float': 1.0,
    'keyspace_hits': 0,
    'keyspace_misses': 0,
}


def test_with_unreacheable_server():
    """
    Check if Redis server is unreacheable
    """

    with pytest.raises(RuntimeError) as error:
        resource = ScalarInfoValue(host='foobar')
        next(resource.probe())

    assert 'Error with Redis server connection' in str(error.value)


@pytest.mark.parametrize('metric_name,expected_error_msg', [
    ['bar', '"bar": Unknown info metric name'],
    ['foo', '"foo" value is not an integer or float: "bar"'],
])
def test_invalid_metric_or_value(mocker, metric_name, expected_error_msg):
    """
    Check if needed info key not exists or having not numeric value
    """

    class FakeStrictRedis(mocker.MagicMock):
        """
        StrictRedis magicmock class with info() method
        """

        def info(self):
            """
            Return fake redis info data

            :returns: fake info data
            :rtype: dict
            """
            self.foo()

            return REDIS_INFO_MOCK


    with mocker.patch(
        'temelio_monitoring.resource.database.'
        'redis.scalar_info_value.StrictRedis',
        new_callable=FakeStrictRedis), \
        pytest.raises(RuntimeError) as error:

        resource = ScalarInfoValue(metric_name=metric_name)

        next(resource.probe())

    assert expected_error_msg in str(error.value)


@pytest.mark.parametrize('metric_name,expected_metric', [
    ['foobar_int', Metric('foobar_int', 1, context='foobar_int')],
    ['foobar_float', Metric('foobar_float', 1.0, context='foobar_float')],
    ['hit_rate', Metric('hit_rate', 0, context='hit_rate')],
])
def test_with_valid_metrics(mocker, metric_name, expected_metric):
    """
    Check if needed info key not exists or having not numeric value
    """

    class FakeStrictRedis(mocker.MagicMock):
        """
        StrictRedis magicmock class with info() method
        """

        def info(self):
            """
            Return fake redis info data

            :returns: fake info data
            :rtype: dict
            """
            self.foo()

            return REDIS_INFO_MOCK


    with mocker.patch(
        'temelio_monitoring.resource.database.'
        'redis.scalar_info_value.StrictRedis',
        new_callable=FakeStrictRedis):

        resource = ScalarInfoValue(metric_name=metric_name)
        metric = next(resource.probe())

        assert metric.name == expected_metric.name
        assert metric.value == expected_metric.value
        assert metric.context == expected_metric.context


def test_with_another_hit_rate(mocker):
    """
    Check if needed info key not exists or having not numeric value
    """

    class FakeStrictRedis(mocker.MagicMock):
        """
        StrictRedis magicmock class with info() method
        """

        def info(self):
            """
            Return fake redis info data

            :returns: fake info data
            :rtype: dict
            """

            self.foo()
            hit_rate_test = REDIS_INFO_MOCK
            hit_rate_test['keyspace_hits'] = 90
            hit_rate_test['keyspace_misses'] = 10

            return REDIS_INFO_MOCK


    with mocker.patch(
        'temelio_monitoring.resource.database.'
        'redis.scalar_info_value.StrictRedis',
        new_callable=FakeStrictRedis):

        expected_metric = Metric('hit_rate', 0.9, context='hit_rate')
        resource = ScalarInfoValue(metric_name='hit_rate')
        metric = next(resource.probe())

        assert metric.name == expected_metric.name
        assert metric.value == expected_metric.value
        assert metric.context == expected_metric.context
