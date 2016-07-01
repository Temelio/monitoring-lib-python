"""
This module manage certificate file argument
"""

from argparse import ArgumentParser


class CertificateFileParser(ArgumentParser):
    """
    Manage certificate file authentication argument parser
    """

    def __init__(self, **kwargs):

        super().__init__(add_help=False)

        # Argument group
        group = self.add_argument_group('Authentication')

        # Argument settings
        group.add_argument(
            '--certificate-file',
            action=kwargs.get('action', 'store'),
            type=kwargs.get('type', str),
            default=kwargs.get('default', ''),
            help=kwargs.get('help', 'Certificate file if required'),
            required=kwargs.get('required', False))
