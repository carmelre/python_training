from python_training.document_gen import document_gen
import json
import hashlib
from elasticsearch import helpers


def index_directory(directory, es_client, index, doc_type, mappings=None):
    """
    Indexes the metadata of the files within the given directory.
    If the given index doesnt exist, it would be created.
    If document file exists in the DB (all fields are the same) we won't save doubles.

    :param directory: The directory which files would be processed.
    :param es_client: A connection object to the target Elasticsearch.
    :param index: The target index to which we will index the documents.
    :param doctype: The doctype of the index and documents.
    :param mappings: The mappings of the index, necessary only if the index doesnt exist.
    """
    if not es_client.indices.exists(index):
        if mappings is None:
            raise ValueError('No mappings were given, the index cannot be created')
        es_client.indices.create(index)
        es_client.indices.put_mapping(doc_type, mappings, index=index)
    result = helpers.bulk(es_client, document_gen(directory, doc_type=doc_type), index=index)
    es_client.indices.refresh(index)
    return result






