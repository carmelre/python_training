import datetime as dt
from typing import List
from collections import defaultdict
from netaddr import valid_ipv4


def index(data: List, redis_connection):
    """
    Inserts the entries into redis sorted sets.
    A set would be created for each ip (with the ip as the key), and the epoch timestamp would be given as a score.
    The set itself would include strings comprised of the epoch timestamp and the protocol, comma separated.

    :param data: A list of 'Entry' instances to index.
    :param redis_connection: An instantiated redis.Redis object.
    """
    ip_to_values = defaultdict(list)
    for entry in data:
        epoch_sec = str(int(entry.timestamp.timestamp()))
        value_to_append = [f'{epoch_sec},{entry.protocol}', f'-{epoch_sec}']
        ip_to_values[entry.ip] += value_to_append
    for ip, values in ip_to_values.items():
        redis_connection.zadd(ip, *values)


def get_device_histogram(ip: str, number_of_results: int, redis_connection):
    """
    Return the latest 'n' entries for the given 'ip'.

    :param ip: The ip of which results would be returned.
    :param number_of_results: The number of result that should be returned.
    :param redis_connection: An instantiated redis.Redis object.

    """
    raw_results = redis_connection.zrange(ip, 0, number_of_results - 1)
    formatted_results = [result.decode().split(',') for result in raw_results]
    return [
        {'timestamp': dt.datetime.fromtimestamp(int(result[0])), 'protocol': result[1]} for result in formatted_results
    ]


def get_devices_status(redis_connection):
    """
    Return a list of every ip and the latest time it was seen it.

    :param redis_connection: An instantiated redis.Redis object.
    """
    ips = redis_connection.keys()
    latest_timestamp_per_ip = {ip: redis_connection.zrange(ip, 0, 1)[0].decode().split(',')[0] for ip in ips}
    return [(ip.decode(), dt.datetime.fromtimestamp(int(timestamp)))
            for ip , timestamp in latest_timestamp_per_ip.items() if valid_ipv4(ip.decode())]
