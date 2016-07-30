"""
This module manage the ExpireDay context
"""


from nagiosplugin import ScalarContext


class ExpireDay(ScalarContext):
    """
    ExpireDay context class
    """

    def __init__(self, *args, **kwargs):

        # Call parent class controller
        super().__init__(*args, **kwargs)

        # Customize output
        self.fmt_metric = ('%s: {value} day(s) left.' %
                           self.name.replace('_', ' ').capitalize())
