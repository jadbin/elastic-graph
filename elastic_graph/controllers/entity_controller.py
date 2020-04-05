# coding=utf-8

from typing import List

from guniflask.web import blueprint, get_route, post_route, put_route, delete_route, RequestBody

from elastic_graph.views.base_view import EntityView
from elastic_graph.views.entity_search import EntitySearchQueryView


@blueprint('/api')
class EntityController:
    @post_route('/entities')
    def create_entity(self, entity_view: EntityView = RequestBody):
        # TODO
        pass

    @post_route('/_bulk/entities')
    def bulk_create_entities(self, entity_view: List[EntityView] = RequestBody):
        # TODO
        pass

    @put_route('/entities/<entity_id>')
    def update_entity(self, entity_id: str, entity_view: EntityView = RequestBody, by_local: bool = False):
        # TODO
        pass

    @delete_route('/entities/<entity_id>')
    def delete_entity(self, entity_id: str):
        # TODO
        pass

    @delete_route('/entities/by-label')
    def delete_entities_by_label(self, labels: str):
        # TODO
        pass

    @get_route('/entities/<entity_id>')
    def get_entity(self, entity_id: str, by_local: bool = False):
        # TODO
        pass

    @post_route('/_search/entities/by-query')
    def search_entities_by_query(self, query: EntitySearchQueryView = RequestBody):
        # TODO
        pass

    @post_route('/entities/<entity_id>/find-parents')
    def find_parents(self, entity_id: str):
        # TODO
        pass

    @post_route('/entities/<entity_id>/find-children')
    def find_children(self, entity_id: str):
        # TODO
        pass

    @post_route('/entities/<entity_id>/find-neighbors')
    def find_neighbors(self, entity_id: str):
        # TODO
        pass
