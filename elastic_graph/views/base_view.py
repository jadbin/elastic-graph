# coding=utf-8


class EntityView:
    id: str
    local_id: str
    entity_name: str
    entity_type: str
    properties: dict
    free_properties: dict
    labels: list

    def to_dict(self):
        return {'id': self.id,
                'local_id': self.local_id,
                'entity_name': self.entity_name,
                'entity_type': self.entity_type,
                'properties': self.properties,
                'free_properties': self.free_properties,
                'labels': self.labels}


class RelationView:
    head_entity_id: str
    tail_entity_id: str
    relation_type: str

    def to_dict(self):
        return {'head_entity_id': self.head_entity_id,
                'tail_entity_id': self.tail_entity_id,
                'relation_type': self.relation_type}
