"""
Blocked client thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.client import BlockedClientParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(crit_blocked_client=50, warn_blocked_client=25)"),
    (
        ['--warn-blocked-client', '20'],
        "Namespace(crit_blocked_client=50, warn_blocked_client=20)"
    ),
    (
        ['--crit-blocked-client', '60'],
        "Namespace(crit_blocked_client=60, warn_blocked_client=25)"
    ),
    (
        ['--warn-blocked-client', '600', '--crit-blocked-client', '900'],
        "Namespace(crit_blocked_client=900, warn_blocked_client=600)"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = BlockedClientParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = BlockedClientParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
