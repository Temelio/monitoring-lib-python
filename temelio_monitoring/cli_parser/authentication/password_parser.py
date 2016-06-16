"""
This module manage password argument
"""

from argparse import ArgumentParser


class PasswordParser(ArgumentParser):
    """
    Manage password authentication argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Authentication')

        # Argument settings
        group.add_argument(
            '--password',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            default=kwargs.get('default', ''),
            help=kwargs.get('help', 'Password if required'),
            required=kwargs.get('required', False))
