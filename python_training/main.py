import os
from python_training.indexing_utils import index_directory
from python_training.mappings import FILE_METADATA_DEFAULT_MAPPING
from python_training.container_management import run_elasticsearch, remove_and_stop_elasticsearch


DIRECTORY_TO_INDEX = f'{os.getcwd()}/directory_to_index'
INDEX = 'carmels_host_file_metadata'
DOCTYPE = 'file_metadata'


if __name__ == '__main__':
    connection, container = run_elasticsearch()
    index_directory(DIRECTORY_TO_INDEX, connection, INDEX, DOCTYPE, mappings=FILE_METADATA_DEFAULT_MAPPING)
    remove_and_stop_elasticsearch(container)

