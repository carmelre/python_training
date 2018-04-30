import os
from elasticsearch import Elasticsearch
from python_training.config import ELASTICSEARCH_INSTANCE
from python_training.indexing_utils import index_directory
from python_training.mappings import FILE_METADATA_DEFAULT_MAPPING

DIRECTORY_TO_INDEX = f'{os.getcwd()}/directory_to_index'
ES_CONNECTION = Elasticsearch(ELASTICSEARCH_INSTANCE)
INDEX = 'carmels_host_file_metadata'
DOCTYPE = 'file_metadata'


if __name__ == '__main__':
    index_directory(DIRECTORY_TO_INDEX, ES_CONNECTION, INDEX, DOCTYPE, mappings=FILE_METADATA_DEFAULT_MAPPING)

