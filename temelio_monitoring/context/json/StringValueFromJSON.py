"""
This module manage String value testing context for data from JSON
"""

from nagiosplugin import Context
from nagiosplugin import Ok, Critical

from temelio_monitoring.utils import ContextUtils
from temelio_monitoring.utils import OperatorUtils


class StringValueFromJSON(Context):
    """
    StringValueFromJSON context class
    """

    def __init__(self, name, expected_string='', operator='=='):
        """
        Init method used by subclass

        :param name: Context name
        :param expected_string: Expected string return by JSON path
        :param operator: Operator to compare probe value with expected string
        :type name: str
        :type expected_string: str
        :type operator: str
        """

        # Call parent class controller
        super().__init__(name)

        # Expected string value
        self._expected_string = expected_string

        # Manage operator used to compare strings
        self._operator = OperatorUtils.get_operator(operator)
        self._operator_str = operator

        # Base output
        self.fmt_metric = (
            "{name}: {value} "
            "(expected string: {expected} // operator used: {operator})"
        )


    def describe(self, metric):
        """
        Manage base context output

        :param metric: Metric returned by probe
        :type metric: nagiosplugin.Metric
        :returns: String representation of context result
        :rtype: str
        """

        value = None

        if len(metric.value) > 0:
            value = metric.value[0].value

        return self.fmt_metric.format(
            expected=self._expected_string,
            name=metric.name.replace('_', ' ').capitalize(),
            operator=self._operator_str,
            value=value
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

        # Extract value from JSON path result
        value = ContextUtils.manage_value_from_json(metric.value)

        # Do compare between metric value and expected string
        result = self._operator(self._expected_string, value)

        if result:
            return self.result_cls(Ok, '', metric)

        return self.result_cls(Critical, '', metric)
