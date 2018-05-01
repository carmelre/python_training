import pytest
from python_training.container_management import run_elasticsearch, remove_and_stop_elasticsearch
from python_training.indexing_utils import index_directory
from python_training.document_gen import filename_gen
from python_training.mappings import FILE_METADATA_DEFAULT_MAPPING
from python_training.tests.mock_data import TEST_DIR_WALK_RESULT
from python_training.document_gen import document_gen
import os

current_work_dir = os.getcwd()

TEST_CONTAINER_NAME = 'elasticsearch-test'
DATA_PORT = 9201
MASTER_PORT = 9301
TEST_DIR_TO_INDEX = 'test_directory_to_index'
TEST_INDEX = 'metadata_test'
TEST_DOCTYPE = 'metadata_test'
FULL_TEST_DIR = f'{current_work_dir}/{TEST_DIR_TO_INDEX}'


@pytest.fixture(scope='session')
def elasticsearch_test():
    connection, container = run_elasticsearch(name=TEST_CONTAINER_NAME, data_port=DATA_PORT, master_port=MASTER_PORT)
    yield connection
    remove_and_stop_elasticsearch(container)


def test_filename_collection():
    filename_gen_result = list(filename_gen(FULL_TEST_DIR))
    assert all([wanted_result in filename_gen_result for wanted_result in TEST_DIR_WALK_RESULT])


def test_insert_without_duplications(elasticsearch_test):
    index_directory(FULL_TEST_DIR, elasticsearch_test, TEST_INDEX, TEST_DOCTYPE, FILE_METADATA_DEFAULT_MAPPING)
    index_directory(FULL_TEST_DIR, elasticsearch_test, TEST_INDEX, TEST_DOCTYPE, FILE_METADATA_DEFAULT_MAPPING)
    assert elasticsearch_test.count(index=TEST_INDEX)['count'] == len(TEST_DIR_WALK_RESULT)
    assert len(elasticsearch_test.indices.get('*')) == 1


def test_indexed_data_validation(elasticsearch_test):
    index_directory(FULL_TEST_DIR, elasticsearch_test, TEST_INDEX, TEST_DOCTYPE, FILE_METADATA_DEFAULT_MAPPING)
    original_docs = document_gen(FULL_TEST_DIR, TEST_DOCTYPE)
    all_docs_query_result = elasticsearch_test.search(index=TEST_INDEX)['hits']['hits']
    for original_doc in original_docs:
        retrieved_doc = [result for result in all_docs_query_result if result['_id'] == original_doc['_id']][0]
        assert original_doc.items() >= retrieved_doc['_source'].items()