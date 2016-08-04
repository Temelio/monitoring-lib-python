"""
This ressource get commands stats info values
"""


from nagiosplugin import CheckError
from nagiosplugin import Cookie
from nagiosplugin import Metric
from nagiosplugin import Resource

from redis import StrictRedis
from redis.exceptions import RedisError


class GetCommandsStats(Resource):
    """
    This ressource get commands stats from redis information about commands
    """

    def __init__(self, **kwargs):
        """
        Initialize ressource attributes

        :param database_id: Redis database id
        :param host: Redis server ip address or fqdn
        :param port: Redis server listening port
        :param password: Password of username authorized to view stats
        :type databse_id: int
        :type host: string
        :type port: int
        :type password: string
        """

        # Arguments management
        self.database_id = kwargs.get('database_id', 0)
        self.host = kwargs.get('host', '127.0.0.1')
        self.password = kwargs.get('password', '')
        self.port = kwargs.get('port', 6379)
        self.probe_state_file = kwargs.get('probe_state_file', None)

        if self.probe_state_file is None:
            raise CheckError('Probe state file is mandatory')

        self.redis_infos = {}


    def probe(self):
        """
        Get information data about commands stats and return Metric objects

        :return: a generator with informations
        :rtype: generator
        """

        try:
            # Connect to redis server
            redis_client = StrictRedis(
                db=self.database_id, host=self.host,
                password=self.password, port=self.port)

            # Get statistics
            self.redis_infos = redis_client.info(section='commandstats')
        except RedisError as error:
            raise CheckError(
                'Error with Redis server connection: {}'.format(str(error)))

        # Manage probe cookie file data
        with Cookie(self.probe_state_file) as state_file:

            # Iterate over all commands stats
            for stat_name, stat_new_values in self.redis_infos.items():

                # Manage file data
                stat_old_values = state_file.get(stat_name)
                if stat_old_values is None:
                    stat_old_values = {'calls': 0, 'usec': 0}
                state_file[stat_name] = stat_new_values

                # Manage reset or restart
                use_new_values = False
                if stat_old_values.get('calls', 0) > stat_new_values['calls']:
                    use_new_values = True

                # Manage metrics
                for metric_name in ['calls', 'usec']:
                    if use_new_values:
                        metric_value = stat_new_values[metric_name]
                    else:
                        metric_value = (stat_new_values[metric_name]
                                        - stat_old_values[metric_name])

                    yield Metric(
                        'db{}_{}.{}'.format(
                            self.database_id, stat_name, metric_name),
                        metric_value,
                        context='default')
