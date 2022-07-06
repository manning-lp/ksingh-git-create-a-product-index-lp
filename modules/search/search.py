from elasticsearch import Elasticsearch
from datetime import datetime
import os
import logging

search_log = logging.getLogger("search")

ALIAS_NAME = "sneakers"
HOST = os.environ.get('ELASTICSEARCH_HOST', 'http://localhost:9200')
es = Elasticsearch(hosts=[HOST])


def get_elasticsearch_health():
    """
    Use this endpoint to check if Elasticsearch is available.
    :return:
    """
    health = es.cluster.health()
    search_log.info(f'Cluster health: {health["status"]}')
    return health


def create_elasticsearch_index(index_body):
    """
    Create a new index using the provided index configuration. Name of the index is a combination of the configured
    ALIAS_NAME and a time stamp in the format of YearMonthDayHourMinuteSecond. Before the index is created, a check is
    done for an existing alias. If the alias exists, it is thrown away. After the index is created, a new Alias is
    created to that specific index.
    :param index_body: JSON object containing the index configuration (mapping and settings)
    :return: The result of the alias creation
    """
    search_log(f'Creating a new index with the name TODO')