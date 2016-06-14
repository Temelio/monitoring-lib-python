# -*- coding: utf-8 -*-

"""
CountValuesFromJSON class tests
-------------------------------

Tests for `CountValuesFromJSON` class.
"""

import pytest

from jsonpath_rw.jsonpath import DatumInContext
from nagiosplugin import Context, Metric, Ok, Warn, Critical

from temelio_monitoring.context.json import CountValuesFromJSON


@pytest.mark.parametrize('warning,critical,exp_state', [
    (0, 0, Ok),
    ('1:', 2, Warn),
    ('1:', '2:', Critical)
])
def test_eval_without_value(warning, critical, exp_state):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = CountValuesFromJSON(
        'foobar',
        warning=warning,
        critical=critical)
    metric = Metric('foobar', [], context='foobar')
    result = context.evaluate(metric, None)

    assert isinstance(context, Context) is True
    assert isinstance(context, CountValuesFromJSON) is True
    assert result.state == exp_state
    assert context.describe(result.metric) == 'Foobar: 0 ([])'
    assert context.performance(result.metric, None).label == 'foobar'
    assert context.performance(result.metric, None).value == 0


@pytest.mark.parametrize('warning,critical,exp_state', [
    (0, 0, Ok),
    (2, 3, Ok),
    ('@1', 2, Warn),
    (0, '@1', Critical)
])
def test_eval_with_one_value(warning, critical, exp_state):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = CountValuesFromJSON(
        'foobar',
        warning=warning,
        critical=critical)
    result_array = [DatumInContext('foo')]
    metric = Metric('foobar', result_array, context='foobar')
    result = context.evaluate(metric, None)

    assert isinstance(context, Context) is True
    assert isinstance(context, CountValuesFromJSON) is True
    assert result.state == exp_state
    assert context.describe(result.metric) == "Foobar: 1 (['foo'])"
    assert context.performance(result.metric, None).label == 'foobar'
    assert context.performance(result.metric, None).value == 1


@pytest.mark.parametrize('warning,critical,exp_state', [
    (0, 0, Ok),
    (0, 1, Critical),
    (1, 2, Warn),
    (2, 3, Ok)
])
def test_eval_with_multiple_values(warning, critical, exp_state):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = CountValuesFromJSON(
        'foobar',
        warning=warning,
        critical=critical)
    result_array = [DatumInContext('foo'), DatumInContext('bar')]
    metric = Metric('foobar', result_array, context='foobar')
    result = context.evaluate(metric, None)

    assert isinstance(context, Context) is True
    assert isinstance(context, CountValuesFromJSON) is True
    assert result.state == exp_state
    assert context.describe(result.metric) == "Foobar: 2 (['foo', 'bar'])"
    assert context.performance(result.metric, None).label == 'foobar'
    assert context.performance(result.metric, None).value == 2
