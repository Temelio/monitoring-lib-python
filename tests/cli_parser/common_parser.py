"""
Common arguments parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser import CommonParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], 'Namespace(timeout=10, verbose=0)'),
    (['--timeout', '20'], 'Namespace(timeout=20, verbose=0)'),
    (['--verbose', '--verbose'], 'Namespace(timeout=10, verbose=2)'),
    (['--timeout', '15', '--verbose'], 'Namespace(timeout=15, verbose=1)')
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = CommonParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = CommonParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
