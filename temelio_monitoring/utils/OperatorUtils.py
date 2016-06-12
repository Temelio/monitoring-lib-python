"""
This module manage utils functions for operator module
"""

import operator

from nagiosplugin import CheckError


class OperatorUtils(object):
    """
    This is the utils class for operator module
    """

    # Operators mapping with string
    _operators = {
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        '!=': operator.ne
    }


    @staticmethod
    def get_operator(operator_str):
        """
        Return needed operator if managed

        :param operator_str: Operator string representation
        :type operator_str: str
        :returns: Operator function
        :rtype: function
        """

        if operator_str not in OperatorUtils._operators:
            raise CheckError('Operator "{}" not managed'.format(operator_str))

        return OperatorUtils._operators[operator_str]
