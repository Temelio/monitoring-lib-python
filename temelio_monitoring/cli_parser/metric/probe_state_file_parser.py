"""
This module manage probe state file argument
"""

from argparse import ArgumentParser


class ProbeStateFileParser(ArgumentParser):
    """
    Manage probe state file argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Metric')

        # Argument settings
        group.add_argument(
            '--probe-state-file',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            help=kwargs.get('help', 'Probe state file to store last results'),
            required=kwargs.get('required', False))
