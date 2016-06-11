# -*- coding: utf-8 -*-

"""
StringValueFromJSON class tests
-------------------------------

Tests for `StringValueFromJSON` class.
"""


from jsonpath_rw.jsonpath import DatumInContext
from nagiosplugin import Context, Metric, Ok, Critical
import pytest


from temelio_monitoring.context.json import StringValueFromJSON

@pytest.mark.parametrize('expected_string,result,expected_output', [
    ('foo', 'bar',
     'My metric: bar (expected string: foo // operator used: ==)'),
    ('foo', 'foo',
     'My metric: foo (expected string: foo // operator used: ==)'),
    ('5', 5, 'My metric: 5 (expected string: 5 // operator used: ==)'),
    ('5', 5, 'My metric: 5 (expected string: 5 // operator used: ==)'),
])
def test_with_args(expected_string, result, expected_output):
    """
    Check context output
    """

    context = StringValueFromJSON(
        'json_output',
        expected_string=expected_string)
    result_array = [DatumInContext(result)]
    metric = Metric('my_metric', result_array)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringValueFromJSON) is True
    assert context.describe(metric) == expected_output


def test_desc_without_value():
    """
    Check if JSON path request not return result
    """

    context = StringValueFromJSON('json_output', 'foo')
    metric = Metric('my_metric', [])

    result = context.describe(metric)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringValueFromJSON) is True
    assert 'My metric: None' in result


def test_eval_without_value():
    """
    Check if JSON path request not return result
    """

    context = StringValueFromJSON('json_output', 'foo')
    metric = Metric('my_metric', [])

    with pytest.raises(RuntimeError) as err:
        context.evaluate(metric, None)

        assert isinstance(context, Context) is True
        assert isinstance(context, StringValueFromJSON) is True

    assert 'No value returned by probe' in str(err)


@pytest.mark.parametrize(
    'metric_name,expected_string,result,operator,eval_result', [
        ('my_metric', 'foo', 'bar', '==', Critical),
        ('my_metric', 'foo', 'bar', '!=', Ok),
        ('my_metric', 'foo', 'foo', '==', Ok),
        ('my_metric', 'foo', 'foo', '!=', Critical),
        ('my_metric', '5', 5, '==', Critical)
    ]
)
def test_eval_with_value(
        metric_name, expected_string, result, operator, eval_result):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = StringValueFromJSON(
        metric_name,
        expected_string=expected_string,
        operator=operator)
    result_array = [DatumInContext(result)]
    metric = Metric(metric_name, result_array, context=metric_name)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringValueFromJSON) is True
    assert context.evaluate(metric, None).state == eval_result
