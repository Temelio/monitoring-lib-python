"""
This module manage Scalar value testing context for data from JSON
"""

from nagiosplugin import ScalarContext

from temelio_monitoring.utils import ContextUtils


class ScalarValueFromJSON(ScalarContext):
    """
    ScalarValueFromJSON context class
    """

    def evaluate(self, metric, resource):
        """
        Compare probe result and expected value

        :param metric: Metric returned by probe
        :param resource: Resource contains probe
        :type metric: nagiosplugin.Metric
        :type resource: nagiosplugin.Resource
        :returns: Result object of context evaluation
        :rtype: nagiosplugin.Result
        """

        # Extract value from JSON path result
        new_value = ContextUtils.manage_value_from_json(metric.value)

        # Create new metric with extracted values
        new_metric = ContextUtils.replace_metric_value(metric, new_value)

        # Call parent evaluate method with new updated metric
        return super().evaluate(new_metric, resource)
