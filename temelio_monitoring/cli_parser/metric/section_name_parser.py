"""
This module manage section name argument
"""

from argparse import ArgumentParser


class SectionNameParser(ArgumentParser):
    """
    Manage section name argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Metric')

        # Argument settings
        group.add_argument(
            '--section-name',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            help=kwargs.get('help', 'Needed section name'),
            required=kwargs.get('required', False))
