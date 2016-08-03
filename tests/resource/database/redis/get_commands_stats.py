# -*- coding: utf-8 -*-

"""
GetCommandsStats class tests
----------------------------

Tests for `GetCommandsStats` class.
"""

import json
import os
from tempfile import NamedTemporaryFile

from nagiosplugin import Metric
import pytest

from temelio_monitoring.resource.database.redis import GetCommandsStats


REDIS_INFO_MOCK = {
    'command_1': {
        'calls': 10,
        'usec': 200,
        'usec_per_call': 20
    },
    'command_2': {
        'calls': 1,
        'usec': 30,
        'usec_per_call': 30
    }
}


def test_without_probe_stat_file():
    """
    Check if Redis server is unreacheable
    """

    with pytest.raises(RuntimeError) as error:
        resource = GetCommandsStats(host='foobar')
        next(resource.probe())

    assert 'Probe state file is mandatory' in str(error.value)


def test_with_unreacheable_server():
    """
    Check if Redis server is unreacheable
    """

    with pytest.raises(RuntimeError) as error:
        resource = GetCommandsStats(host='foobar', probe_state_file='foobar')
        next(resource.probe())

    assert 'Error with Redis server connection' in str(error.value)


@pytest.mark.parametrize('state_file_content,expected_metrics', [
    [
        b'{}',
        [
            Metric('db0_command_1.calls', 10, context='default'),
            Metric('db0_command_1.usec', 200, context='default'),
            Metric('db0_command_2.calls', 1, context='default'),
            Metric('db0_command_2.usec', 30, context='default'),
        ]
    ],
    [
        (b'{"command_1":{"calls":5,"usec":100,"used_per_call":20},'
         b'"command_2":{"calls":1,"usec":30,"used_per_call":30}}'),
        [
            Metric('db0_command_1.calls', 5, context='default'),
            Metric('db0_command_1.usec', 100, context='default'),
            Metric('db0_command_2.calls', 0, context='default'),
            Metric('db0_command_2.usec', 0, context='default'),
        ]
    ],
    [
        (b'{"command_1":{"calls":50,"usec":500,"used_per_call":10},'
         b'"command_2":{"calls":2,"usec":30,"used_per_call":15}}'),
        [
            Metric('db0_command_1.calls', 10, context='default'),
            Metric('db0_command_1.usec', 200, context='default'),
            Metric('db0_command_2.calls', 1, context='default'),
            Metric('db0_command_2.usec', 30, context='default'),
        ]
    ],
])
def test_with_valid_metrics(mocker, state_file_content, expected_metrics):
    """
    Check if needed info key not exists or having not numeric value
    """

    class FakeStrictRedis(mocker.MagicMock):
        """
        StrictRedis magicmock class with info() method
        """

        def info(self, section=''):
            """
            Return fake redis info data

            :returns: fake info data
            :rtype: dict
            """
            self.foo(section)

            return REDIS_INFO_MOCK


    with mocker.patch(
        'temelio_monitoring.resource.database.'
        'redis.get_commands_stats.StrictRedis',
        new_callable=FakeStrictRedis), \
        NamedTemporaryFile(delete=False) as tmp_file:

        # Write fake content in temporary file
        tmp_file.write(state_file_content)
        tmp_file.close()

        resource = GetCommandsStats(probe_state_file=tmp_file.name)

        all_metrics = sorted(resource.probe())
        metric_index = 0

        # Check metrics returned by probe
        for metric in all_metrics:
            assert metric.name == expected_metrics[metric_index].name
            assert metric.value == expected_metrics[metric_index].value
            assert metric.context == expected_metrics[metric_index].context
            metric_index += 1

        # Check state file content after probe execution
        with open(tmp_file.name) as tmp_file_reopen:
            tmp_file_content = json.load(tmp_file_reopen)

        assert tmp_file_content['command_1']['calls'] == 10
        assert tmp_file_content['command_1']['usec'] == 200
        assert tmp_file_content['command_1']['usec_per_call'] == 20
        assert tmp_file_content['command_2']['calls'] == 1
        assert tmp_file_content['command_2']['usec'] == 30
        assert tmp_file_content['command_2']['usec_per_call'] == 30

    os.unlink(tmp_file.name)
