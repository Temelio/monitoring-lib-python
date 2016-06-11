# -*- coding: utf-8 -*-

"""
StringEqualityFromJSON class tests
----------------------------------

Tests for `StringEqualityFromJSON` class.
"""


from jsonpath_rw.jsonpath import DatumInContext
from nagiosplugin import Context, Metric, Ok, Critical
import pytest


from temelio_monitoring.context import StringEqualityFromJSON

@pytest.mark.parametrize('expected_string,result,do_cast,expected_output', [
    ('foo', 'bar', False,
     'My metric: bar (expected string: foo // do_str_cast: False)'),
    ('foo', 'foo', False,
     'My metric: foo (expected string: foo // do_str_cast: False)'),
    ('5', 5, True,
     'My metric: 5 (expected string: 5 // do_str_cast: True)'),
    ('5', 5, False,
     'My metric: 5 (expected string: 5 // do_str_cast: False)'),
])
def test_with_args(expected_string, result, do_cast, expected_output):
    """
    Check context output
    """

    context = StringEqualityFromJSON(
        'json_output',
        expected_string=expected_string,
        do_str_cast=do_cast)
    result_array = [DatumInContext(result)]
    metric = Metric('my_metric', result_array)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringEqualityFromJSON) is True
    assert context.describe(metric) == expected_output


def test_desc_without_value():
    """
    Check if JSON path request not return result
    """

    context = StringEqualityFromJSON('json_output', 'foo', False)
    metric = Metric('my_metric', [])

    result = context.describe(metric)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringEqualityFromJSON) is True
    assert 'My metric: None' in result


def test_eval_without_value():
    """
    Check if JSON path request not return result
    """

    context = StringEqualityFromJSON('json_output', 'foo', False)
    metric = Metric('my_metric', [])

    with pytest.raises(RuntimeError) as err:
        context.evaluate(metric, None)

        assert isinstance(context, Context) is True
        assert isinstance(context, StringEqualityFromJSON) is True

    assert 'No value returned by probe' in str(err)


@pytest.mark.parametrize(
    'metric_name,expected_string,result,do_cast,eval_result', [
        ('my_metric', 'foo', 'bar', False, Critical),
        ('my_metric', 'foo', 'foo', False, Ok),
        ('my_metric', '5', 5, True, Ok),
        ('my_metric', '5', 5, False, Critical)
    ]
)
def test_eval_with_cast(metric_name, expected_string, result, do_cast,
                        eval_result):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = StringEqualityFromJSON(
        metric_name,
        expected_string=expected_string,
        do_str_cast=do_cast)
    result_array = [DatumInContext(result)]
    metric = Metric(metric_name, result_array, context=metric_name)

    assert isinstance(context, Context) is True
    assert isinstance(context, StringEqualityFromJSON) is True
    assert context.evaluate(metric, None).state == eval_result
