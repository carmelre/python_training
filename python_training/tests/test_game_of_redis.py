import pytest
from python_training import redis_management
from python_training.tests.mock_data import MOCK_DATA_SET, MOCK_DATA_BASE
from python_training import implement_me

REDIS_CONF_TEMPLATE = 'redis_test_template.conf'
REDIS_TEST_NAME = 'redis-test'
REDIS_TEST_PORT = 6370


@pytest.fixture(scope='session')
def redis_test_db():
    connection, container = redis_management.run_redis(REDIS_TEST_NAME, REDIS_TEST_PORT)
    yield connection
    redis_management.remove_and_stop_redis(container)


def test_index_data(redis_test_db):
    implement_me.index(MOCK_DATA_SET, redis_test_db)


def test_get_device_histogram(redis_test_db):
    result = implement_me.get_device_histogram('1.1.1.1', 2, redis_test_db)
    manual_result = [{'timestamp': mock_data[2], 'protocol': mock_data[1]} for mock_data in MOCK_DATA_BASE[1:3]]
    manual_result.reverse()
    assert result == manual_result


def test_get_device_status(redis_test_db):
    result = implement_me.get_devices_status(redis_test_db)
    manual_results = [(data[0], data[2]) for data in MOCK_DATA_BASE[-2:]]
    assert all([manual_result in result for manual_result in manual_results])
