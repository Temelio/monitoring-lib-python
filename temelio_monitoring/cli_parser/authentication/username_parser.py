"""
This module manage username argument
"""

from argparse import ArgumentParser


class UsernameParser(ArgumentParser):
    """
    Manage username authentication argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Authentication')

        # Argument settings
        group.add_argument(
            '--username',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            default=kwargs.get('default', ''),
            help=kwargs.get('help', 'Username if required'),
            required=kwargs.get('required', False))
