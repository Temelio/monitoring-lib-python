"""
This module manage metric name argument
"""

from argparse import ArgumentParser


class MetricNameParser(ArgumentParser):
    """
    Manage metric name argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Metric')

        # Argument settings
        group.add_argument(
            '--metric-name',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            help=kwargs.get('help', 'Needed metric name'),
            required=kwargs.get('required', False))
