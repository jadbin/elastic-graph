# coding=utf-8

from typing import List

from guniflask.context import service
from guniflask.config import settings

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from elastic_graph.views.base_view import EntityView


@service
class ElasticSearchService:
    free_property_delimiter = '\xa0'

    def __init__(self):
        self.es = Elasticsearch(settings.get('elastic_search_hosts'))

    def _get_index(self, entity_type: str):
        return 'elastic_graph.entity.{}'.format(entity_type)

    def create_document(self, entity_view: EntityView):
        source = self._get_source_from_entity_view(entity_view)
        self.es.index(self._get_index(entity_view.entity_type),
                      source,
                      id=entity_view.id)

    def create_documents(self, entity_views: List[EntityView]):
        data = [{
            '_op_type': 'index',
            '_index': self._get_index(entity_view.entity_type),
            '_id': entity_view.id,
            '_source': self._get_source_from_entity_view(entity_view)

        } for entity_view in entity_views]
        bulk(self.es, data)

    def update_document(self, entity_view: EntityView):
        self.create_document(entity_view)

    def get_document(self, entity_type: str, entity_id: str) -> EntityView:
        resp = self.es.get(self._get_index(entity_type), entity_id)
        return self._read_entity_view_from_source(resp['_source'])

    def delete_document(self, entity_type: str, entity_id: str):
        self.es.delete(self._get_index(entity_type), entity_id)

    def delete_documents(self, entity_types: List[str], entity_ids: List[str]):
        data = []
        n = len(entity_types)
        for i in range(n):
            data.append({
                '_op_type': 'delete',
                '_index': self._get_index(entity_types[i]),
                '_id': entity_ids[i]
            })
        bulk(self.es, data)

    def search_documents_by_query(self, query: str) -> List[EntityView]:
        body = {
            'query': {
                'bool': {
                    'must': {
                        'simple_query_string': {
                            'query': query
                        }
                    }
                }
            },
            'from': 0,
            'size': 100
        }
        params = {'timeout': '20s'}
        result = self.es.search(body=body, index='elastic_graph.entity.*', params=params)
        entities = []
        for obj in result['hits']['hits']:
            entities.append(self._read_entity_view_from_source(obj['_source']))
        return entities

    def _get_source_from_entity_view(self, entity_view: EntityView):
        source = {
            'id': entity_view.id,
            'local_id': entity_view.local_id,
            'entity_type': entity_view.entity_type,
            'entity_name': entity_view.entity_name,
            'properties': entity_view.properties,
            'free_properties': self._format_free_properties(entity_view.free_properties),
            'labels': self._format_labels(entity_view.labels)
        }
        return source

    def _format_free_properties(self, props: dict) -> List[str]:
        result = []
        if props is None:
            return result
        for p in props:
            vlist = props[p]
            if not isinstance(vlist, list):
                vlist = [vlist]
            for v in vlist:
                s = '{}{}{}'.format(p, self.free_property_delimiter, v)
                result.append(s)
        return result

    def _format_labels(self, labels: list) -> List[str]:
        if labels is None:
            return []
        return list(labels)

    def _read_entity_view_from_source(self, source: dict):
        entity_view = EntityView()
        entity_view.id = source['id']
        entity_view.local_id = source['local_id']
        entity_view.entity_type = source['entity_type']
        entity_view.entity_name = source['entity_name']
        entity_view.properties = source['properties']
        entity_view.free_properties = self._read_free_properties(source['free_properties'])
        entity_view.labels = source['labels']
        return entity_view

    def _read_free_properties(self, props: List[str]) -> dict:
        result = {}
        for p in props:
            s = p.split(self.free_property_delimiter, maxsplit=1)
            if s[0] not in result:
                result[s[0]] = s[1]
            else:
                v = result[s[0]]
                if not isinstance(v, list):
                    v = [v]
                    result[s[0]] = v
                v.append(s[1])
        return result
