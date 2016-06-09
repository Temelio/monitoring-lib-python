"""
This module manage the ConnectionsCount context
"""


from nagiosplugin import ScalarContext


class ConnectionCount(ScalarContext):
    """
    ConnectionCount context class
    """

    def __init__(self, *args, **kwargs):

        # Call parent class controller
        super().__init__(*args, **kwargs)

        # Customize output
        self.fmt_metric = ('%s: {value}' %
                           self.name.replace('_', ' ').capitalize())
