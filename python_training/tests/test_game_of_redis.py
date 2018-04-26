import pytest
from python_training import redis_management

REDIS_CONF_TEMPLATE = 'redis_test_template.conf'
REDIS_TEST_NAME = 'redis-test'
REDIS_TEST_PORT = 6370


@pytest.fixture(scope='session')
def redis_test_db():
    connection, container = redis_management.run_redis(REDIS_TEST_NAME, REDIS_TEST_PORT)
    yield connection
    redis_management.remove_and_stop_redis(container)


def test_simple(redis_test_db):
    connection = redis_test_db



