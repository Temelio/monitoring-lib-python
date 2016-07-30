"""
This module manage connected client arguments
"""

from argparse import ArgumentParser


class ConnectedClientParser(ArgumentParser):
    """
    Manage connected client thresholds argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Thresholds')

        # Argument settings
        group.add_argument(
            '--warn-connected-client',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 25),
            help=kwargs.get('help', 'Connected client warning threshold'),
            required=kwargs.get('required', False))

        # Argument settings
        group.add_argument(
            '--crit-connected-client',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 50),
            help=kwargs.get('help', 'Connected client critical threshold'),
            required=kwargs.get('required', False))
