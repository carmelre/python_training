import docker
from elasticsearch import Elasticsearch
import time
import contextlib
import sys
import os
from python_training.config import DEFAULT_MASTER_PORT, DEFAULT_CONTAINER_NAME, \
    DEFAULT_DATA_PORT, IMAGE_NAME, ES_SERVER

CLIENT = docker.from_env()
MAX_CONNECTION_ATTEMPTS = 10
CONNECTION_ATTEMPT_INTERVAL = 2


@contextlib.contextmanager
def no_stderr():
    """
    Redirects stderr to dev null, and reverts when the context is exited.
    """
    original_stderr = sys.stderr
    with open(os.devnull, 'w') as pipe:
        sys.stderr = pipe
        try:
            yield
        finally:
            sys.stderr = original_stderr


def run_elasticsearch(name=DEFAULT_CONTAINER_NAME, data_port=DEFAULT_DATA_PORT, master_port=DEFAULT_MASTER_PORT):
    """
    Runs an elasticsearch container and returns a connection to the DB.
    :param: name: The name that would be given to the container.
    :param: data_port: The port would be bound to the default es data port within the container.
    :param: master_port: The port would be bound to the default es master port within the container.
    :return: An Elasticseatch client, and the es container object.
    """
    container = CLIENT.containers.run(IMAGE_NAME,
                                      ports={f'{DEFAULT_DATA_PORT}/tcp': data_port,
                                             f'{DEFAULT_MASTER_PORT}/tcp': master_port},
                                      detach=True,
                                      name=name,
                                      environment=['discovery.type=single-node'])
    elasticsearch_connection = Elasticsearch(f'{ES_SERVER}:{data_port}')
    number_of_attempts = 0
    while number_of_attempts != MAX_CONNECTION_ATTEMPTS:
        with no_stderr():
            elasticsearch_response = elasticsearch_connection.ping()
        if elasticsearch_response is True:
            return elasticsearch_connection, container
        time.sleep(CONNECTION_ATTEMPT_INTERVAL)
        number_of_attempts += 1
    raise ConnectionError('Max number of attempts to connect to the elasticsearch service has been reached')


def remove_and_stop_elasticsearch(container):
    """
    Stops and removes the Elasticsearch container.
    """
    container.stop()
    container.remove()
