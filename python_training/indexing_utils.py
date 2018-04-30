from python_training.document_gen import document_gen
import json
import hashlib


def index_directory(directory, es_connection, index, doctype, mappings=None):
    """
    Indexes the metadata of the files within the given directory.
    If the given index doesnt exist, it would be created.
    If document file exists in the DB (all fields are the same) we won't save doubles.

    :param directory: The directory which files would be processed.
    :param es_connection: A connection object to the target Elasticsearch.
    :param index: The target index to which we will index the documents.
    :param doctype: The doctype of the index and documents.
    :param mappings: The mappings of the index, necessary only if the index doesnt exist.
    """
    if not es_connection.indices.exists(index):
        if mappings is None:
            raise ValueError('No mappings were given, the index cannot be created')
        es_connection.indices.create(index)
        es_connection.indices.put_mapping(doctype, mappings, index=index)
    for document in document_gen(directory):
        es_connection.index(index, doctype, document, id=hashlib.md5(json.dumps(document).encode()).hexdigest())





