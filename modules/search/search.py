import json
from elasticsearch import Elasticsearch
from datetime import datetime
import os
import logging

search_log = logging.getLogger("search")

ALIAS_NAME = "sneakers"
HOST = os.environ.get("ELASTICSEARCH_HOST", "http://localhost:9200")
es = Elasticsearch(hosts=[HOST])


def get_elasticsearch_health():
    """
    Use this endpoint to check if Elasticsearch is available.
    :return:
    """
    health = es.cluster.health()
    search_log.info(f'Cluster health: {health["status"]}')
    return health


def create_elasticsearch_index():
    """
    Create a new index. Name of the index is a combination of the configured ALIAS_NAME and a time stamp in the format
    of YearMonthDayHourMinuteSecond. Before the index is created, we remove it if it already exists. The settings
    and mappings are obtained from the shoes_index.json in the config folder.
    :return: The name of the created index
    """
    index_name = f"{ALIAS_NAME}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    search_log.info(f"Creating a new index with the name {index_name}")
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../config/shoes_index.json"
    )
    json_object = None
    try:
        with open(file_path, "r") as file:
            json_object = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file: {file_path}")
        return None
    if es.indices.exists(index=index_name):
        search_log.info(f"Removing index {index_name} because it already exists")
        es.indices.delete(index=index_name)
    es.indices.create(
        index=index_name,
        body=json_object,
    )
    search_log.info(f"Index {index_name} created")
    return index_name


def index_shoe(shoe, index_name):
    """
    Send the provided shoe to Elasticsearch to index that shoe into the provided index.
    :param shoe: The Shoe to index
    :param index_name: The index to use for indexing the shoe
    :return:
    """
    search_log.info(f'Indexing shoe: {shoe["id"]} into index with name {index_name}')
    es.index(index=index_name, document=shoe)


def switch_alias_to(index_name):
    """
    Checks if the alias as configured is already available, if so, remove all indexes it points to. When finished add
    the provided index to the alias.
    :param index_name: Name of the index to assign to the alias
    :return:
    """
    search_log.info(f"Assign alias {ALIAS_NAME} to {index_name}")
    try:
        response = es.indices.get_alias(name=ALIAS_NAME)
        indices = list(response.keys())
        print(f"Alias '{ALIAS_NAME}' points to index/indices: {indices}")
    except Exception as e:
        print(f"Error: {e}")

    actions = {
        "actions": [
            {"remove": {"index": "*", "alias": ALIAS_NAME}},
            {"add": {"index": index_name, "alias": ALIAS_NAME}},
        ]
    }
    try:
        es.indices.update_aliases(body=actions)
        print(f"Alias '{ALIAS_NAME}' updated to point to '{index_name}'")
    except Exception as e:
        print(f"Failed to update alias: {e}")
    search_log.info(f"Alias {ALIAS_NAME} now points to {index_name}")
    return True
