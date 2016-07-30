"""
Connected client thresholds argument parser tests
"""

import pytest
from capturer import CaptureOutput

from temelio_monitoring.cli_parser.client import ConnectedClientParser


@pytest.mark.parametrize('arguments,expected_output', [
    ([], "Namespace(crit_connected_client=50, warn_connected_client=25)"),
    (
        ['--warn-connected-client', '20'],
        "Namespace(crit_connected_client=50, warn_connected_client=20)"
    ),
    (
        ['--crit-connected-client', '60'],
        "Namespace(crit_connected_client=60, warn_connected_client=25)"
    ),
    (
        ['--warn-connected-client', '600', '--crit-connected-client', '900'],
        "Namespace(crit_connected_client=900, warn_connected_client=600)"
    )
])
def test_parser(arguments, expected_output):
    """
    Check with valid arguments
    """

    parser = ConnectedClientParser()
    assert str(parser.parse_args(arguments)) == expected_output


def test_parser_bad_argument():
    """
    Check with an unknown argument
    """

    parser = ConnectedClientParser()

    with pytest.raises(SystemExit) as sys_exit, CaptureOutput() as capture:
        parser.parse_args(['--foo'])

    assert sys_exit.value.code == 2
    assert 'unrecognized arguments: --foo' in capture.get_text()
