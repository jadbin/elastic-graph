# coding=utf-8

from typing import List

from guniflask.web import blueprint, post_route, delete_route, RequestBody

from elastic_graph.views.base_view import RelationView


@blueprint('/api')
class RelationController:

    @post_route('/relations')
    def create_relation(self, relation_view: RelationView = RequestBody, by_local: bool = False):
        # TODO
        pass

    @post_route('/_bulk/relations')
    def bulk_create_relations(self, relation_view: List[RelationView] = RequestBody, by_local: bool = False):
        # TODO
        pass

    @delete_route('/relations')
    def delete_relation(self, relation_view: RelationView = RequestBody, by_local: bool = False):
        pass
