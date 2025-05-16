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
    search_log.info(f"Creating a new index with the name TODO")
    # TODO M3: Implement this function


def index_shoe(shoe, index_name):
    """
    Send the provided shoe to Elasticsearch to index that shoe into the provided index.
    :param shoe: The Shoe to index
    :param index_name: The index to use for indexing the shoe
    :return:
    """
    search_log.info(f'Indexing shoe: {shoe["id"]} into index with name {index_name}')
    # TODO M2: Implement this function
    res = es.index(index=index_name, document=shoe)
    print(res["result"])


def switch_alias_to(index_name):
    """
    Checks if the alias as configured is already available, if so, remove all indexes it points to. When finished add
    the provided index to the alias.
    :param index_name: Name of the index to assign to the alias
    :return:
    """
    search_log.info(f"Assign alias {ALIAS_NAME} to {index_name}")
    # TODO M3: Implement this function
