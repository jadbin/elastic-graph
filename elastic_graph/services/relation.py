# coding=utf-8

from typing import List

from guniflask.context import service

from elastic_graph.views.base_view import RelationView
from .elastic_search import ElasticSearchService
from .neo4j import Neo4jService


@service
class RelationService:

    def __init__(self, es: ElasticSearchService, neo4j: Neo4jService):
        self.es = es
        self.neo4j = neo4j

    def create_relation(self, relation_view: RelationView):
        self.neo4j.create_relation(relation_view)

    def create_relations(self, relation_views: List[RelationView]):
        self.neo4j.create_relations(relation_views)

    def delete_relation(self, relation_view: RelationView):
        return self.neo4j.delete_relation(relation_view)
