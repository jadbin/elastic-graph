# coding=utf-8

from guniflask.context import service
from guniflask.config import settings

from elasticsearch import Elasticsearch


@service
class ElasticSearchService:
    def __init__(self):
        self.es = Elasticsearch(settings.get('elastic_search_hosts'))
