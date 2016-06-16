"""
Waiting connection thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.connection import WaitingConnectionParser


@pytest.mark.parametrize('arguments,expected_output', [
    (
        [],
        "Namespace(crit_waiting_connection=1000, warn_waiting_connection=500)"
    ),
    (
        ['--warn-waiting-connection', '600'],
        "Namespace(crit_waiting_connection=1000, warn_waiting_connection=600)"
    ),
    (
        ['--crit-waiting-connection', '1200'],
        "Namespace(crit_waiting_connection=1200, warn_waiting_connection=500)"
    ),
    (
        ['--warn-waiting-connection', '600',
         '--crit-waiting-connection', '900'],
        "Namespace(crit_waiting_connection=900, warn_waiting_connection=600)"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = WaitingConnectionParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = WaitingConnectionParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
