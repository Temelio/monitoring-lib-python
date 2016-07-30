"""
This module manage port argument
"""

from argparse import ArgumentParser


class PortParser(ArgumentParser):
    """
    Manage port setting argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Location')

        # Argument settings
        group.add_argument(
            '--port',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', int),
            help=kwargs.get('help', 'Host port'),
            required=kwargs.get('required', False))
