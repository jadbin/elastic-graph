# coding=utf-8

from typing import List

from flask import abort

from guniflask.web import blueprint, post_route, RequestBody

from elastic_graph.views.base_view import RelationView
from elastic_graph.services.relation import RelationService
from elastic_graph.models import BaseEntity


@blueprint('/api')
class RelationController:

    def __init__(self, relation_service: RelationService):
        self.relation_service = relation_service

    @post_route('/relations')
    def create_relation(self, relation_view: RelationView = RequestBody, by_local: bool = False):
        head_entity = self._get_base_entity(relation_view.head_entity_id, by_local=by_local)
        tail_entity = self._get_base_entity(relation_view.tail_entity_id, by_local=by_local)
        relation_view.head_entity_id = head_entity.id
        relation_view.tail_entity_id = tail_entity.id
        self.relation_service.create_relation(relation_view)
        return 'success'

    @post_route('/_bulk/relations')
    def bulk_create_relations(self, relation_views: List[RelationView] = RequestBody, by_local: bool = False):
        for r in relation_views:
            head_entity = self._get_base_entity(r.head_entity_id, by_local=by_local)
            tail_entity = self._get_base_entity(r.tail_entity_id, by_local=by_local)
            r.head_entity_id = head_entity.id
            r.tail_entity_id = tail_entity.id
        self.relation_service.create_relations(relation_views)
        return 'success'

    @post_route('/relations/delete')
    def delete_relation(self, relation_view: RelationView = RequestBody, by_local: bool = False):
        head_entity = self._get_base_entity(relation_view.head_entity_id, by_local=by_local)
        tail_entity = self._get_base_entity(relation_view.tail_entity_id, by_local=by_local)
        relation_view.head_entity_id = head_entity.id
        relation_view.tail_entity_id = tail_entity.id
        self.relation_service.delete_relation(relation_view)
        return 'success'

    def _get_base_entity(self, entity_id, by_local=False) -> BaseEntity:
        if by_local:
            base_entity = BaseEntity.query.filter_by(local_id=entity_id).first()
        else:
            base_entity = BaseEntity.query.filter_by(id=entity_id).first()
        if not base_entity:
            abort(404)
        return base_entity
