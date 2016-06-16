# -*- coding: utf-8 -*-

"""
ConnectionCount class tests
--------------------------

Tests for `ConnectionCount` class.
"""


from nagiosplugin import ScalarContext, Metric
import pytest


from temelio_monitoring.context.connection import ConnectionCount


def test_without_args():
    """
    Check if try to use context without arguments
    """

    with pytest.raises(TypeError) as error:
        ConnectionCount()

    assert 'missing 1 required positional argument' in str(error.value)


@pytest.mark.parametrize('context_name,expected_output', [
    ('foo', 'Foo: 5'),
    ('foo_bar', 'Foo bar: 5'),
    ('foo-bar', 'Foo-bar: 5'),
])
def test_with_args(context_name, expected_output):
    """
    Check context output
    """

    context = ConnectionCount(context_name, 2, 3)
    metric = Metric('my_metric', 5)

    assert isinstance(context, ScalarContext) is True
    assert context.describe(metric) == expected_output
