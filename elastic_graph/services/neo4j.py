# coding=utf-8

import logging
from typing import List, Dict, Union
from collections import defaultdict

from guniflask.context import service
from guniflask.beans import SmartInitializingSingleton
from guniflask.config import settings

from neo4j import GraphDatabase, Driver, Session, BoltStatementResult

from elastic_graph.views.base_view import EntityView, RelationView

log = logging.getLogger(__name__)


@service
class Neo4jService(SmartInitializingSingleton):
    def __init__(self):
        self.neo4j: Driver = None

    def after_singletons_instantiated(self):
        try:
            self.neo4j = GraphDatabase.driver(settings.get('neo4j_uri'),
                                              auth=settings.get('neo4j_auth'))
        except Exception:
            log.error('Failed to connect neo4j', exc_info=True)

    def create_node(self, entity_view: EntityView):
        q = 'CREATE (:Entity:`{}`{} {{entity_id:"{}"}})'.format(entity_view.entity_type,
                                                                self._labels_to_append(entity_view.labels),
                                                                entity_view.id)
        session: Session = self.neo4j.session()
        session.run(q)
        session.close()

    def create_nodes(self, entity_views: List[EntityView]):
        q = 'CREATE ' + ', '.join(
            ['(:Entity:`{}`{} {{entity_id:"{}"}})'.format(entity_view.entity_type,
                                                          self._labels_to_append(entity_view.labels),
                                                          entity_view.id)
             for entity_view in entity_views])
        session: Session = self.neo4j.session()
        session.run(q)
        session.close()

    def update_node(self, entity_view: EntityView):
        q = 'MATCH (n:Entity {{ entity_id:"{}" }}) RETURN labels(n)'.format(entity_view.id)
        session: Session = self.neo4j.session()
        ret: BoltStatementResult = session.run(q)

        old_labels = ret.value('labels(n)')[0]
        q2 = 'MATCH (n:Entity {{ entity_id:"{}" }}) REMOVE n{} ' \
             'SET n:Entity{}'.format(entity_view.id,
                                     self._labels_to_append(old_labels),
                                     self._labels_to_append(entity_view.labels))
        session.run(q2)
        session.close()

    def delete_node(self, entity_id: str):
        q = 'MATCH (n:Entity {{ entity_id:"{}" }}) DELETE n'.format(entity_id)
        session: Session = self.neo4j.session()
        session.run(q)
        session.close()

    def delete_nodes(self, entity_ids: List[str]):
        q = 'UNWIND $id_list AS i MATCH (n:Entity {entity_id:i}) DELETE n'
        params = {'id_list': entity_ids}
        session: Session = self.neo4j.session()
        session.run(q, parameters=params)
        session.close()

    def delete_node_relations(self, entity_id: str):
        q1 = 'MATCH (n:Entity)-[r]->(m:Entity {{ entity_id:"{}" }}) DELETE r'.format(entity_id)
        q2 = 'MATCH (n:Entity {{ entity_id:"{}" }})-[r]->(m:Entity) DELETE r'.format(entity_id)
        session: Session = self.neo4j.session()
        session.run(q1)
        session.run(q2)
        session.close()

    def delete_relations_of_nodes(self, entity_ids: List[str]):
        q1 = 'UNWIND $id_list AS i MATCH (n:Entity)-[r]->(m:Entity { entity_id: i }) DELETE r'
        q2 = 'UNWIND $id_list AS i MATCH (n:Entity { entity_id: i })-[r]->(m:Entity) DELETE r'
        params = {'id_list': entity_ids}
        session: Session = self.neo4j.session()
        session.run(q1, parameters=params)
        session.run(q2, parameters=params)
        session.close()

    def create_relation(self, relation_view: RelationView):
        q = 'MATCH (h:Entity {{entity_id:"{}"}}), (t:Entity {{entity_id:"{}"}}) ' \
            'MERGE (h)-[r:`{}`]->(t)'.format(relation_view.head_entity_id,
                                             relation_view.tail_entity_id,
                                             relation_view.relation_type)
        session: Session = self.neo4j.session()
        session.run(q)
        session.close()

    def create_relations(self, relation_views: List[RelationView]):
        views = self._collect_relations_by_type(relation_views)
        session: Session = self.neo4j.session()
        for relation_type in views:
            q = 'UNWIND $relations AS r ' \
                'MATCH (h:Entity {{entity_id:r.head_entity_id}}), (t:Entity {{entity_id:r.tail_entity_id}}) ' \
                'MERGE (h)-[:`{}`]->(t)'.format(relation_type)
            relations = [{'head_entity_id': r.head_entity_id, 'tail_entity_id': r.tail_entity_id}
                         for r in views[relation_type]]
            params = {'relations': relations}
            session.run(q, parameters=params)
        session.close()

    def delete_relation(self, relation_view: RelationView):
        q = 'MATCH (n:Entity {{ entity_id:"{}" }})-[r:`{}`]->(m:Entity {{ entity_id:"{}" }}) ' \
            'DELETE r'.format(relation_view.head_entity_id, relation_view.relation_type, relation_view.tail_entity_id)
        session: Session = self.neo4j.session()
        session.run(q)
        session.close()

    def find_parents(self, entity_id: str) -> Dict[str, str]:
        q = 'MATCH (h:Entity)-[r]->(t:Entity {{entity_id:"{}"}}) RETURN h.entity_id, type(r)'.format(entity_id)
        session: Session = self.neo4j.session()
        ret: BoltStatementResult = session.run(q)
        session.close()
        result = {}
        for r in ret:
            result[r['h.entity_id']] = r['type(r)']
        return result

    def find_children(self, entity_id: str) -> Dict[str, str]:
        q = 'MATCH (h:Entity {{entity_id:"{}"}})-[r]->(t:Entity) RETURN t.entity_id, type(r)'.format(entity_id)
        session: Session = self.neo4j.session()
        ret: BoltStatementResult = session.run(q)
        session.close()
        result = {}
        for r in ret:
            result[r['t.entity_id']] = r['type(r)']
        return result

    def _labels_to_append(self, labels: Union[list, set]):
        if not labels:
            return ''
        return ''.join([':`{}`'.format(l) for l in labels])

    def _collect_relations_by_type(self, relation_views: List[RelationView]) -> Dict[str, List[RelationView]]:
        result = defaultdict(list)
        for relation_view in relation_views:
            result[relation_view.relation_type].append(relation_view)
        return result
