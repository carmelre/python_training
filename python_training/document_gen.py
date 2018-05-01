import os
from datetime import datetime
import json
import hashlib


def convert_timestamp(timestamp: float) -> str:
    """
    Converts a given timestamp to a string in the format that would be displayed in elasticsearch (yyyy-mm-dd hh-mm-ss).

    :param timestamp: The timestamp that would be converted.
    :return: A string representation of the timestamp.
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def filename_gen(directory: str) -> tuple:
    """
    Generates the path and filename of all the files in a given directory (recursively).

    :param directory: The directory that would be walked upon.
    :return: Each iteration a tuple containing a single path and filename is returned.
    """
    for path, dirs, file_names in os.walk(directory):
        for file_name in file_names:
            yield path, file_name


def create_metadata(path: str, file_name: str) -> dict:
    """
    Creates an dictionary containing the metadata of the given file.
    The dictionary represents a single file in elasticsearch.

    :param path: The path of the file
    :param file_name: The name of the file.
    :return: A dictionary containing the files metadata that would be indexed.
    """
    raw_meta = os.stat(f'{path}/{file_name}')
    return {'size': raw_meta.st_size,
                   'mode': raw_meta.st_mode,
                   'uid': raw_meta.st_uid,
                   'gid': raw_meta.st_gid,
                   'path': path,
                   'file_name': file_name,
                   'access time': convert_timestamp(raw_meta.st_atime),
                   'modification time': convert_timestamp(raw_meta.st_mtime),
                   'change time': convert_timestamp(raw_meta.st_ctime)}


def directory_validator(directory: str):
    """
    Validates that the given path is absilute (we dont want relative paths in our DB), and that is exists.

    :param directory: The directory containing the files we want to index.
    """
    if directory.startswith('.'):
        raise ValueError('The path is not absolute')
    if not os.path.exists(directory):
        raise ValueError('The path does not exist')


def document_gen(directory: str, doc_type: str) -> dict:
    """
    Generates a dictionary for each file in the directory, representing a single elasticsearch document.
    The dictionary contains the metadata that we parse and index.

    :param directory: The directory which files would be processed.
    :param doc_type: The elasticseatch doctype that would be filled in the _type field.
    At the moment only one doctype is supported per directory.
    :return: a dictionary containing formatted metadata data of each file in the directory.
    """
    directory_validator(directory)
    for path, file_name in filename_gen(directory):
        es_document = create_metadata(path, file_name)
        es_document['_id'] = hashlib.md5(json.dumps(es_document).encode()).hexdigest()
        es_document['_type'] = doc_type
        yield es_document
