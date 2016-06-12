"""
This module manage element count testing context for data from JSON
"""

from nagiosplugin import ScalarContext

from temelio_monitoring.utils import ContextUtils


class CountValuesFromJSON(ScalarContext):
    """
    ScalarValueFromJSON context class
    """

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Store extracted values
        self._values = []

        # Base output
        self.fmt_metric = (
            "{name}: {count} "
            "({values})"
        )


    def describe(self, metric):
        """
        Manage base context output

        :param metric: Metric returned by probe
        :type metric: nagiosplugin.Metric
        :returns: String representation of context result
        :rtype: str
        """

        return self.fmt_metric.format(
            count=metric.value,
            name=metric.name.replace('_', ' ').capitalize(),
            values=str(self._values)
        )


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

        # Extract values from JSON path result
        self._values = ContextUtils.manage_values_from_json(metric.value)

        # Create new metric with extracted values
        new_metric = ContextUtils.replace_metric_value(metric,
                                                       len(self._values))

        # Call parent evaluate method with new updated metric
        return super().evaluate(new_metric, resource)
