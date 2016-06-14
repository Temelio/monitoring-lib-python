# -*- coding: utf-8 -*-

"""
ScalarValueFromJSON class tests
-------------------------------

Tests for `ScalarValueFromJSON` class.
"""

import pytest

from jsonpath_rw.jsonpath import DatumInContext
from nagiosplugin import Context, Metric, Ok, Warn, Critical

from temelio_monitoring.context.json import ScalarValueFromJSON


@pytest.mark.parametrize(
    'metric_name,warning,critical,result,eval_result', [
        ('my_metric', 1, 2, 3, Critical),
        ('my_metric', 1, 2, 2, Warn),
        ('my_metric', 1, 2, 1, Ok)
    ]
)
def test_eval_with_value(
        metric_name, warning, critical, result, eval_result):
    """
    Check evaluate method, Ressource param not used, so set it to None
    """

    context = ScalarValueFromJSON(
        metric_name,
        warning=warning,
        critical=critical)
    result_array = [DatumInContext(result)]
    metric = Metric(metric_name, result_array, context=metric_name)

    assert isinstance(context, Context) is True
    assert isinstance(context, ScalarValueFromJSON) is True
    assert context.evaluate(metric, None).state == eval_result
