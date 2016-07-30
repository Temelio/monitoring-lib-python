"""
Host argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.location import HostParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(host='127.0.0.1')"),
    (
        ['--host', 'foobar'],
        "Namespace(host='foobar')"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = HostParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = HostParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
