"""
Key file argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.authentication import KeyFileParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(key_file='')"),
    (['--key-file', 'foo'], "Namespace(key_file='foo')")
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = KeyFileParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = KeyFileParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
