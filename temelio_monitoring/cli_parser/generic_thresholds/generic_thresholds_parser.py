"""
This module manage argparse arguments to use generic thresholds
"""

from argparse import ArgumentParser


class GenericThresholdsParser(ArgumentParser):
    """
    Manage common options argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False, **kwargs)

        group = self.add_argument_group('Thresholds')
        group.add_argument(
            '--warning',
            action='store',
            type=str,
            help='Warning threshold')

        group.add_argument(
            '--critical',
            action='store',
            type=str,
            help='Critical threshold')
