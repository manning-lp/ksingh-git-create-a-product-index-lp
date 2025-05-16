from search import (
    get_elasticsearch_health,
    create_elasticsearch_index,
    index_shoe,
    switch_alias_to,
)
from bs4 import BeautifulSoup
from pprint import pprint

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


def import_shoes_from_file(file_name):
    """
    Import shoes from a file containing a shoe on each line. Use the index_shoe function of the search module to index
    :param file_name: The name of the file to import shoes from.
    :return:
    """
    index_name = create_elasticsearch_index()
    _do_import_shoes_from_file(file_name=file_name, index_name=index_name)
    switch_alias_to(index_name)


def _do_import_shoes_from_file(file_name, index_name):
    logging.info(
        f"Start importing shoes from the file: {file_name} into index {index_name}"
    )
    with open(file_name, "r") as file:
        file_content = file.readlines()
        for line in file_content:
            json_line = json.loads(line)
            soup = BeautifulSoup(json_line["description"], "html.parser")
            json_line["description"] = soup.get_text()
            index_shoe(json_line, "sneakers")

        print(f"Number of shoes to import: {len(file_content)}")
