"""
URL argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.web import UrlParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(url='')"),
    (['--url', 'foo'], "Namespace(url='foo')")
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = UrlParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = UrlParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
