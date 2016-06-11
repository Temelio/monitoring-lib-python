"""
This module manage String equality testing context for data from JSON
"""

from nagiosplugin import CheckError
from nagiosplugin import Context
from nagiosplugin import Ok, Critical


class StringEqualityFromJSON(Context):
    """
    StringEqualityFromJSON context class
    """

    def __init__(self, name, expected_string='', do_str_cast=False):
        """
        Init method used by subclass

        :param name: Context name
        :param expected_string: Expected string return by JSON path
        :param do_str_cast: If True, use str() on value returned by JSON path
        :type name: str
        :type expected_string: str
        :type do_str_cast: bool
        """

        # Call parent class controller
        super().__init__(name)

        # Expected string value
        self._expected_string = expected_string

        # Do an str cast before evaluate value
        self._do_str_cast = do_str_cast

        # Base output
        self.fmt_metric = (
            "{name}: {value} "
            "(expected string: {expected} // do_str_cast: {do_str_cast})"
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
            do_str_cast=self._do_str_cast,
            expected=self._expected_string,
            name=metric.name.replace('_', ' ').capitalize(),
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

        if len(metric.value) == 0:
            raise CheckError(RuntimeError('No value returned by probe'))

        value = metric.value[0].value

        if self._do_str_cast is True:
            result = str(self._expected_string) == str(value)
        else:
            result = self._expected_string == value

        if result:
            return self.result_cls(Ok, '', metric)

        return self.result_cls(Critical, '', metric)
