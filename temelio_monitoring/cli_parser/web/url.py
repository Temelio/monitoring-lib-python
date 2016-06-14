"""
This module manage URL argument
"""

from argparse import ArgumentParser


class UrlParser(ArgumentParser):
    """
    Manage URL argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Target')

        # Argument settings
        group.add_argument(
            '--url',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            default=kwargs.get('default', ''),
            help=kwargs.get('help', 'URL target'),
            required=kwargs.get('required', False))
