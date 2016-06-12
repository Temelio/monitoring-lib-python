"""
This module manage element count testing context for data from JSON
"""

from nagiosplugin import Metric, ScalarContext


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

        # Manage JSON path results
        if len(metric.value) != 0:
            for element in metric.value:
                self._values.append(element.value)

        # Extract value from JSON path result
        new_metric = Metric(
            metric.name,
            len(self._values),
            context=metric.context,
            contextobj=metric.contextobj,
            resource=metric.resource)

        # Call parent evaluate method with new updated metric
        return super().evaluate(new_metric, resource)
