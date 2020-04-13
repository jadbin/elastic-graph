# coding=utf-8

from typing import List

from guniflask.web import blueprint, get_route, post_route, put_route, delete_route, RequestBody

from flask import jsonify, abort

from elastic_graph.views.base_view import EntityView
from elastic_graph.views.entity_search import EntitySearchQueryView
from elastic_graph.services.base_entity import BaseEntityService
from elastic_graph.models import BaseEntity


@blueprint('/api')
class EntityController:
    def __init__(self, entity_service: BaseEntityService):
        self.entity_service = entity_service

    @post_route('/entities')
    def create_entity(self, entity_view: EntityView = RequestBody):
        local_id = entity_view.local_id
        base_entity = BaseEntity.query.filter_by(local_id=local_id).first()
        if base_entity is not None:
            entity_view.id = base_entity.id
            return self.update_entity(base_entity.id, entity_view)
        base_entity = self.entity_service.create_entity(entity_view)
        data = {'id': base_entity.id}
        return jsonify(data)

    @post_route('/_bulk/entities')
    def bulk_create_entities(self, entity_views: List[EntityView] = RequestBody):
        result = [None] * len(entity_views)
        prepare = []
        for i, entity_view in enumerate(entity_views):
            local_id = entity_view.local_id
            base_entity = BaseEntity.query.filter_by(local_id=local_id).first()
            if base_entity is not None:
                entity_view.id = base_entity.id
                self.update_entity(base_entity.id, entity_view)
                result[i] = base_entity
            else:
                prepare.append(entity_view)
        prepare_entities = self.entity_service.create_entities(prepare)
        i = 0
        for e in prepare_entities:
            while result[i] is not None:
                i += 1
            result[i] = e

        data = [{'id': e.id} for e in prepare_entities]
        return jsonify(data)

    @put_route('/entities/<entity_id>')
    def update_entity(self, entity_id: str, entity_view: EntityView = RequestBody, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        entity_view.id = base_entity.id
        self.entity_service.update_entity(base_entity, entity_view)
        return 'success'

    @delete_route('/entities/<entity_id>')
    def delete_entity(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        self.entity_service.delete_entity(base_entity)
        return 'success'

    @delete_route('/entities/by-label')
    def delete_entities_by_label(self, labels: str):
        # TODO
        pass

    @get_route('/entities/<entity_id>')
    def get_entity(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        return jsonify(self.entity_service.get_view_of_entity(base_entity).to_dict())

    @post_route('/_search/entities/by-query')
    def search_entities_by_query(self, query_view: EntitySearchQueryView = RequestBody):
        entities = self.entity_service.search_entities_by_query(query_view.query)
        data = [e.to_dict() for e in entities]
        return jsonify(data)

    @post_route('/entities/<entity_id>/find-parents')
    def find_parents(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        return jsonify(self.entity_service.find_entity_parents(base_entity))

    @post_route('/entities/<entity_id>/find-children')
    def find_children(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        return jsonify(self.entity_service.find_entity_children(base_entity))

    @post_route('/entities/<entity_id>/find-neighbors')
    def find_neighbors(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        return jsonify(self.entity_service.find_entity_neighbors(base_entity))

    @delete_route('/entities/<entity_id>/relations')
    def delete_entity_relations(self, entity_id: str, by_local: bool = False):
        base_entity = self._get_base_entity(entity_id, by_local=by_local)
        self.entity_service.delete_entity_relations(base_entity)
        return 'success'

    @delete_route('/entities/_all')
    def delete_entity_relations(self):
        all_entities = BaseEntity.query.all()
        for e in all_entities:
            self.delete_entity_relations(e.id)
            self.delete_entity(e.id)
        return 'success'

    def _get_base_entity(self, entity_id, by_local=False) -> BaseEntity:
        if by_local:
            base_entity = BaseEntity.query.filter_by(local_id=entity_id).first()
        else:
            base_entity = BaseEntity.query.filter_by(id=entity_id).first()
        if not base_entity:
            abort(404)
        return base_entity
