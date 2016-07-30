"""
This module manage host argument
"""

from argparse import ArgumentParser


class HostParser(ArgumentParser):
    """
    Manage host setting argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Location')

        # Argument settings
        group.add_argument(
            '--host',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            default=kwargs.get('default', '127.0.0.1'),
            help=kwargs.get('help', 'Host target'),
            required=kwargs.get('required', False))
