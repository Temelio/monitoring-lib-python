"""
Manage utils methods to use in context classes
"""

from nagiosplugin import CheckError, Metric


class ContextUtils(object):
    """
    Utils methods to use in context classes
    """

    @staticmethod
    def check_size(data, min_size, max_size):
        """
        Check if data contains only one element

        Useful for xxxValueFromJSON context classes

        :param data: Data to validate
        :param min_size: Min size of tested element
        :param max_size: Max size of tested element
        :type data: list|str|dict|tuple
        :type min_size: int
        :type max_size: int
        :returns: Empty string if check is OK, else error message
        :rtype: str
        """

        element_size = len(data)

        if element_size == 0:
            return 'No value returned by probe'

        elif element_size < min_size:
            return 'Less values than expected'

        elif element_size > max_size:
            return 'More values than expected'

        return ''


    @staticmethod
    def manage_value_from_json(metric_value):
        """
        Manage single value expectation in metric from JSON data

        :param metric_value: Metric value
        :type metric_value: list
        :returns: Extracted value from JSON path result
        :rtype: string|int
        """

        # This context only manage one element
        check_result = ContextUtils.check_size(metric_value, 1, 1)
        if check_result:
            raise CheckError(check_result)

        # Get value
        return metric_value[0].value


    @staticmethod
    def manage_values_from_json(metric_values):
        """
        Manage multiple values in metric from JSON data

        :param metric_values: Metric values
        :type metric_values: list
        :returns: Extracted values from JSON path result
        :rtype: list
        """

        values = []

        # Manage JSON path results
        for element in metric_values:
            values.append(element.value)

        return values


    @staticmethod
    def replace_metric_value(metric, new_value):
        """
        Create new metric with value parameter

        :param metric: Metric value
        :type metric: nagiosplugin.Metric
        :returns: New metric with extracted values from JSON path result
        :rtype: nagiosplugin.Metric
        """

        new_metric = Metric(
            metric.name,
            new_value,
            context=metric.context,
            contextobj=metric.contextobj,
            resource=metric.resource)

        # Return metric with values extracted
        return new_metric
