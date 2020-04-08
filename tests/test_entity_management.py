# coding=utf-8

from tests.api import get_entity, create_entities, create_entity, delete_entity, \
    create_relation, delete_entity_relations, delete_relation, \
    find_children, find_parents, find_neighbors


def test_entity_management():
    local_id = 'person_小明'
    local_id1 = local_id + '1'
    local_id2 = local_id + '2'
    name = '小明'
    entity_type = 'person'
    properties = {
        'age': 18,
        'hobbies': ['game', 'food']
    }
    free_properties = {
        '年龄': 18,
        '兴趣': ['游戏', '食物']
    }
    labels = ['student', 'person']
    relation_type = 'some relation'
    relation_type2 = 'some relation 2'

    create_entity(local_id=local_id, entity_type=entity_type, entity_name=name,
                  properties=properties, free_properties=free_properties, labels=labels)

    entity = get_entity(local_id=local_id)
    assert entity['local_id'] == local_id
    assert entity['entity_name'] == '小明'
    assert entity['entity_type'] == 'person'
    assert len(entity['properties']) == 2
    assert entity['properties']['age'] == 18
    assert entity['properties']['hobbies'] == ['game', 'food']
    assert len(entity['free_properties']) == 2
    assert entity['free_properties']['年龄'] == '18'
    assert entity['free_properties']['兴趣'] == ['游戏', '食物']
    assert entity['labels'] == ['student', 'person']

    create_entities(local_id=local_id, entity_type=entity_type, entity_name=name,
                    properties=properties, free_properties=free_properties, labels=labels, n=2)
    entity = get_entity(local_id=local_id1)
    assert entity['local_id'] == local_id1
    assert entity['entity_name'] == '小明'
    assert entity['entity_type'] == 'person'
    assert len(entity['properties']) == 2
    assert entity['properties']['age'] == 18
    assert entity['properties']['hobbies'] == ['game', 'food']
    assert len(entity['free_properties']) == 2
    assert entity['free_properties']['年龄'] == '18'
    assert entity['free_properties']['兴趣'] == ['游戏', '食物']
    assert entity['labels'] == ['student', 'person']

    delete_entity(local_id=local_id1)

    create_relation(head_entity_id=local_id, tail_entity_id=local_id2, relation_type=relation_type, by_local=True)
    create_relation(head_entity_id=local_id2, tail_entity_id=local_id, relation_type=relation_type2, by_local=True)

    parents = find_parents(entity_id=local_id, by_local=True)
    assert len(parents) == 1
    assert parents[0]['relation_type'] == relation_type2
    assert parents[0]['entity']['local_id'] == local_id2

    children = find_children(entity_id=local_id, by_local=True)
    assert len(children) == 1
    assert children[0]['relation_type'] == relation_type
    assert children[0]['entity']['local_id'] == local_id2

    neighbors = find_neighbors(entity_id=local_id, by_local=True)
    parents = neighbors['parents']
    assert len(parents) == 1
    assert parents[0]['relation_type'] == relation_type2
    assert parents[0]['entity']['local_id'] == local_id2
    children = neighbors['children']
    assert len(children) == 1
    assert children[0]['relation_type'] == relation_type
    assert children[0]['entity']['local_id'] == local_id2

    delete_relation(head_entity_id=local_id, tail_entity_id=local_id2, relation_type=relation_type, by_local=True)
    delete_entity_relations(entity_id=local_id, by_local=True)

    delete_entity(local_id=local_id)
    delete_entity(local_id=local_id2)
