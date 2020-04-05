# coding=utf-8

from guniflask.context import service
from guniflask.config import settings

from neo4j import GraphDatabase


@service
class Neo4jService:
    def __init__(self):
        self.neo4j = GraphDatabase.driver(settings.get('neo4j_uri'),
                                          auth=settings.get('neo4j_auth'))
