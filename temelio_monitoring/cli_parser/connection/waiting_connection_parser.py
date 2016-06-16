"""
This module manage waiting connection arguments
"""

from argparse import ArgumentParser


class WaitingConnectionParser(ArgumentParser):
    """
    Manage waiting connection thresholds argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Thresholds')

        # Argument settings
        group.add_argument(
            '--warn-waiting-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 500),
            help=kwargs.get('help', 'Waiting connection warning threshold'),
            required=kwargs.get('required', False))

        # Argument settings
        group.add_argument(
            '--crit-waiting-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 1000),
            help=kwargs.get('help', 'Waiting connection critical threshold'),
            required=kwargs.get('required', False))
