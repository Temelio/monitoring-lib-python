"""
Generic thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.generic_thresholds import \
    GenericThresholdsParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(critical=None, warning=None)"),
    (
        ['--warning', '600'],
        "Namespace(critical=None, warning='600')"
    ),
    (
        ['--critical', '1200'],
        "Namespace(critical='1200', warning=None)"
    ),
    (
        ['--warning', '600', '--critical', '900'],
        "Namespace(critical='900', warning='600')"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = GenericThresholdsParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = GenericThresholdsParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
