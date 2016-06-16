"""
Manage OperatorUtils class testing
"""

import pytest

from nagiosplugin import CheckError
from temelio_monitoring.utils import OperatorUtils


@pytest.mark.parametrize('operand_a,operand_b,operator,expected_result', [
    (2, 1, '>', True),
    (2, 3, '>', False),
    (1, 2, '<', True),
    (2, 2, '<', False),
    (2, 2, '>=', True),
    (3, 2, '>=', True),
    (1, 2, '>=', False),
    (1, 1, '<=', True),
    (2, 2, '<=', True),
    (3, 2, '<=', False),
    (2, 2, '==', True),
    ('foo', 'foo', '==', True),
    (3, 2, '==', False),
    (2, 1, '!=', True),
    ('foo', 'bar', '!=', True),
    (2, 2, '!=', False),
])
def test_operator_mapping(operand_a, operand_b, operator, expected_result):
    """
    Check use of mapped operator
    """

    operator_func = OperatorUtils.get_operator(operator)

    assert operator_func(operand_a, operand_b) == expected_result


def test_unmanaged_operator():
    """
    Check use of unmapped operator
    """

    with pytest.raises(CheckError) as error:
        OperatorUtils.get_operator('foo')

    assert 'Operator "foo" not managed' in str(error)
