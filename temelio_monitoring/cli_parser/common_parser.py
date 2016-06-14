"""
This module manage argparse arguments to define verbosity level
"""

from argparse import ArgumentParser


class CommonParser(ArgumentParser):
    """
    Manage common options argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False, **kwargs)

        group = self.add_argument_group('General settings')
        group.add_argument(
            '--timeout',
            action='store',
            type=int,
            default=10,
            help='Plugin timeout')

        group.add_argument(
            '-v',
            '--verbose',
            action='count',
            default=0,
            help='Script verbosity')
