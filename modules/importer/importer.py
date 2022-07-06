from search import get_elasticsearch_health, create_elasticsearch_index
from bs4 import BeautifulSoup

import json
import logging


logging = logging.getLogger("importer")


def verify_connection():
    """
    Check if we can connect to Elasticsearch.
    :return:
    """
    result = get_elasticsearch_health()
    logging.info(f'Name of Elasticsearch cluster: {result["cluster_name"]}')
    logging.info(f'Status of Elasticsearch cluster: {result["status"]}')
    return result


def refresh_index(index_file_name):
    """
    Refresh the index, uses the file name to find the index configuration and create a new index.
    :return: String containing the result of creating the new index
    """
    logging.info(f'Start refreshing the index using file: {index_file_name}')
    # TODO: Implement this function

def import_shoes_from_file(file_name):
    """
    Import shoes from a file containing a shoe on each line.
    :param file_name: The name of the file.
    :return:
    """
    logging.info(f'Start importing shoes from the file: {file_name}')
    # TODO: Implement this function