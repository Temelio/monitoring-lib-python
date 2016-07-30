"""
This module manage number of days arguments
"""

from argparse import ArgumentParser


class DayCountParser(ArgumentParser):
    """
    Manage number of days thresholds argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Thresholds')

        # Argument settings
        group.add_argument(
            '--warning-nb-days',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 30),
            help=kwargs.get('help', 'Number of days warning threshold'),
            required=kwargs.get('required', False))

        # Argument settings
        group.add_argument(
            '--critical-nb-days',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 15),
            help=kwargs.get('help', 'Number of days critical threshold'),
            required=kwargs.get('required', False))
