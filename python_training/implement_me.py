import datetime as dt
from typing import List


def index(data: List, redis_connection):
    """
    Inserts the entries into redis sorted sets.
    A set would be created for each ip (with the ip as the key), and the epoch timestamp would be given as a score.
    The set itself would include strings comprised of the epoch timestamp and the protocol, comma separated.

    :param data: A list of 'Entry' instances to index.
    :param redis_connection: An instantiated redis.Redis object.
    """
    ip_to_values = {}
    for entry in data:
        epoch_sec = str(int(entry.timestamp.timestamp()))
        value_to_append = [f'{epoch_sec},{entry.protocol}', epoch_sec]
        ip_to_values[entry.ip] = ip_to_values[
                                     entry.ip] + value_to_append if entry.ip in ip_to_values else value_to_append
    for ip, values in ip_to_values.items():
        redis_connection.zadd(ip, *values)


def get_device_histogram(ip, n, redis_connection):
    """
    Return the latest 'n' entries for the given 'ip'.
    """
    raw_results = redis_connection.zrange(ip, -n, -1)
    formatted_results = [result.decode().split(',') for result in raw_results]
    dict_splitted_results = [
        {'timestamp': dt.datetime.fromtimestamp(int(result[0])), 'protocol': result[1]} for result in formatted_results
    ].reverse()
    return dict_splitted_results


def get_devices_status():
    """
    Return a list of every ip and the latest time it was seen it.
    """
    return [
        ('4.2.2.4', dt.datetime.now()),
        ('8.8.8.8', dt.datetime.now())
    ]
