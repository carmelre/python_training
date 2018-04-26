import docker
import redis
import time


CLIENT = docker.from_env()
DEFAULT_PORT = 6379
DEFAULT_CONTAINER_NAME = 'redis'
IMAGE_NAME = 'redis'
MAX_CONNECTION_ATTEMPTS = 3


def run_redis(name=DEFAULT_CONTAINER_NAME, port=DEFAULT_PORT):
    """
    Runs a redis container and returns a connection to the DB.

    :param: name: The name that would be given to the container.
    :param: port: The port on localhost that would be bound to the default redis port within the container.
    :return: A redis connection.
    """
    container = CLIENT.containers.run(IMAGE_NAME, ports={f'{DEFAULT_PORT}/tcp': port}, detach=True, name=name)
    redis_connection = redis.Redis(host='localhost', port=f'{port}')
    number_of_attempts = 0
    while redis_connection.info()['loading'] != 0 and number_of_attempts != MAX_CONNECTION_ATTEMPTS:
        time.sleep(1)
        number_of_attempts += 1
    return redis_connection, container


def remove_and_stop_redis(container):
    """
    Stops and removes the redis container.
    """
    container.stop()
    container.remove()
