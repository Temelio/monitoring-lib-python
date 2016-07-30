"""
This module manage database id argument
"""

from argparse import ArgumentParser


class DatabaseIdParser(ArgumentParser):
    """
    Manage database id argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Database')

        # Argument settings
        group.add_argument(
            '--database-id',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            default=kwargs.get('default', 0),
            help=kwargs.get('help', 'Needed metric name'),
            required=kwargs.get('required', False))
