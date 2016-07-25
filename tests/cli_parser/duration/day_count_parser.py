"""
Day count thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.duration import DayCountParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(critical_nb_days=15, warning_nb_days=30)"),
    (
        ['--warning-nb-days', '25'],
        "Namespace(critical_nb_days=15, warning_nb_days=25)"
    ),
    (
        ['--critical-nb-days', '5'],
        "Namespace(critical_nb_days=5, warning_nb_days=30)"
    ),
    (
        ['--warning-nb-days', '20', '--critical-nb-days', '10'],
        "Namespace(critical_nb_days=10, warning_nb_days=20)"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = DayCountParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = DayCountParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
