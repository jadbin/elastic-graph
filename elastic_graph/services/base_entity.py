# coding=utf-8

import uuid
from typing import List

from guniflask.context import service

from elastic_graph.app import db
from elastic_graph.models.base_entity import BaseEntity
from elastic_graph.views.base_view import EntityView
from .elastic_search import ElasticSearchService
from .neo4j import Neo4jService


@service
class BaseEntityService:

    def __init__(self, es: ElasticSearchService, neo4j: Neo4jService):
        self.es = es
        self.neo4j = neo4j

    def generate_id(self) -> str:
        return uuid.uuid4().hex

    def create_entity(self, entity_view: EntityView) -> BaseEntity:
        base_entity = BaseEntity()
        base_entity.id = self.generate_id()
        entity_view.id = base_entity.id
        self._update_base_entity_by_entity_view(base_entity, entity_view)

        db.session.add(base_entity)
        self.neo4j.create_node(entity_view)
        self.es.create_document(entity_view)
        db.session.commit()
        return base_entity

    def create_entities(self, entity_views: List[EntityView]) -> List[BaseEntity]:
        base_entities = []
        for entity_view in entity_views:
            base_entity = BaseEntity()
            base_entity.id = self.generate_id()
            entity_view.id = base_entity.id
            self._update_base_entity_by_entity_view(base_entity, entity_view)
            base_entities.append(base_entity)

            db.session.add(base_entity)

        self.neo4j.create_nodes(entity_views)
        self.es.create_documents(entity_views)
        db.session.commit()
        return base_entities

    def update_entity(self, base_entity: BaseEntity, entity_view: EntityView):
        self._update_base_entity_by_entity_view(base_entity, entity_view)
        self.neo4j.update_node(entity_view)
        self.es.update_document(entity_view)
        db.session.commit()

    def get_view_of_entity(self, base_entity: BaseEntity) -> EntityView:
        return self.es.get_document(base_entity.entity_type, base_entity.id)

    def find_entity_parents(self, base_entity: BaseEntity) -> list:
        parents = self.neo4j.find_parents(base_entity.id)
        result = []
        for k, t in parents.items():
            entity = BaseEntity.query.filter_by(id=k).first()
            if entity:
                result.append({
                    'relation_type': t,
                    'entity': self.get_view_of_entity(entity).to_dict()
                })
        return result

    def find_entity_children(self, base_entity: BaseEntity) -> list:
        parents = self.neo4j.find_children(base_entity.id)
        result = []
        for k, t in parents.items():
            entity = BaseEntity.query.filter_by(id=k).first()
            if entity:
                result.append({
                    'relation_type': t,
                    'entity': self.get_view_of_entity(entity).to_dict()
                })
        return result

    def find_entity_neighbors(self, base_entity: BaseEntity) -> dict:
        return {
            'parents': self.find_entity_parents(base_entity),
            'children': self.find_entity_children(base_entity)
        }

    def delete_entity(self, base_entity: BaseEntity):
        self.neo4j.delete_node(base_entity.id)
        self.es.delete_document(base_entity.entity_type, base_entity.id)
        db.session.delete(base_entity)
        db.session.commit()

    def delete_entities(self, base_entities: List[BaseEntity]):
        entity_types = [e.entity_type for e in base_entities]
        entity_ids = [e.id for e in base_entities]
        self.neo4j.delete_nodes(entity_ids)
        self.es.delete_documents(entity_types, entity_ids)
        for e in base_entities:
            db.session.delete(e)
        db.session.commit()

    def delete_entity_relations(self, base_entity: BaseEntity):
        self.neo4j.delete_node_relations(base_entity.id)

    def _update_base_entity_by_entity_view(self, base_entity: BaseEntity, entity_view: EntityView):
        base_entity.local_id = entity_view.local_id
        base_entity.entity_type = entity_view.entity_type
