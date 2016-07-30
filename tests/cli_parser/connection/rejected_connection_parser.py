"""
Rejected connection thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.connection import RejectedConnectionParser


@pytest.mark.parametrize('arguments,expected_output', [
    (
        [],
        "Namespace(crit_rejected_connection=50, warn_rejected_connection=25)"
    ),
    (
        ['--warn-rejected-connection', '30'],
        "Namespace(crit_rejected_connection=50, warn_rejected_connection=30)"
    ),
    (
        ['--crit-rejected-connection', '1200'],
        "Namespace(crit_rejected_connection=1200, warn_rejected_connection=25)"
    ),
    (
        ['--warn-rejected-connection', '600',
         '--crit-rejected-connection', '900'],
        "Namespace(crit_rejected_connection=900, warn_rejected_connection=600)"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = RejectedConnectionParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = RejectedConnectionParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
