"""
Manage ContextUtils class testing
"""

import pytest

from temelio_monitoring.utils import ContextUtils


# To have parameters more readeable
NO_VALUE = 'No value returned by probe'
TOO_MANY = 'More values than expected'
TOO_LESS = 'Less values than expected'
VALID = ''

@pytest.mark.parametrize('data,min_size,max_size,expected_result', [
    # List tests
    ([], 1, 1, NO_VALUE),
    (['foo'], 2, 2, TOO_LESS),
    (['foo'], 1, 1, VALID),
    (['foo'], 1, 2, VALID),
    (['foo', 'bar'], 1, 1, TOO_MANY),
    # Tuple tests
    ((), 1, 1, NO_VALUE),
    (('foo',), 1, 1, VALID),
    (('foo',), 1, 2, VALID),
    (('foo', 'bar'), 1, 1, TOO_MANY),
    # Dict tests
    ({}, 1, 1, NO_VALUE),
    ({'foo': 'bar'}, 1, 1, VALID),
    ({'foo': 'bar', 'foo2': 'bar2'}, 1, 2, VALID),
    ({'foo': 'bar', 'foo2': 'bar2'}, 1, 1, TOO_MANY),
    # Str tests
    ('', 1, 1, NO_VALUE),
    ('f', 1, 1, VALID),
    ('fo', 1, 2, VALID),
    ('foo', 1, 1, TOO_MANY),
])
def test_check_size(data, min_size, max_size, expected_result):
    """
    Tests about check_size utils method
    """

    assert ContextUtils.check_size(data, min_size, max_size) == expected_result
