"""
This module manage active connection arguments
"""

from argparse import ArgumentParser


class ActiveConnectionParser(ArgumentParser):
    """
    Manage active connection thresholds argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Thresholds')

        # Argument settings
        group.add_argument(
            '--warn-active-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 500),
            help=kwargs.get('help', 'Active connection warning threshold'),
            required=kwargs.get('required', False))

        # Argument settings
        group.add_argument(
            '--crit-active-connection',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 1000),
            help=kwargs.get('help', 'Active connection critical threshold'),
            required=kwargs.get('required', False))
