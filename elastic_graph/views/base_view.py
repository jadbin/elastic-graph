# coding=utf-8


class EntityView:
    id: str
    local_id: str
    entity_name: str
    entity_type: str
    properties: list
    free_properties: list
    labels: set


class RelationView:
    head_entity_id: str
    tail_entity_id: str
    relation_type: str
