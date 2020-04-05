# coding=utf-8

from urllib.parse import quote

import requests

base_url = 'http://localhost:6660/api'


def test_entity_management():
    local_id = 'person_小明'
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

    _create_entity(local_id=local_id, entity_type=entity_type, entity_name=name,
                   properties=properties, free_properties=free_properties, labels=labels)

    entity = _get_entity(local_id=local_id)
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

    _create_entity(local_id=local_id2, entity_type=entity_type, entity_name=name,
                   properties=properties, free_properties=free_properties, labels=labels)

    _create_relation(head_entity_id=local_id, tail_entity_id=local_id2, relation_type=relation_type, by_local=True)
    _create_relation(head_entity_id=local_id2, tail_entity_id=local_id, relation_type=relation_type2, by_local=True)

    parents = _find_parents(entity_id=local_id, by_local=True)
    assert len(parents) == 1
    assert parents[0]['relation_type'] == relation_type2
    assert parents[0]['entity']['local_id'] == local_id2

    children = _find_children(entity_id=local_id, by_local=True)
    assert len(children) == 1
    assert children[0]['relation_type'] == relation_type
    assert children[0]['entity']['local_id'] == local_id2

    neighbors = _find_neighbors(entity_id=local_id, by_local=True)
    parents = neighbors['parents']
    assert len(parents) == 1
    assert parents[0]['relation_type'] == relation_type2
    assert parents[0]['entity']['local_id'] == local_id2
    children = neighbors['children']
    assert len(children) == 1
    assert children[0]['relation_type'] == relation_type
    assert children[0]['entity']['local_id'] == local_id2

    _delete_relation(head_entity_id=local_id, tail_entity_id=local_id2, relation_type=relation_type, by_local=True)
    _delete_entity_relations(entity_id=local_id, by_local=True)

    _delete_entity(local_id=local_id)
    _delete_entity(local_id=local_id2)


def _create_entity(local_id: str = None, entity_type: str = None, entity_name: str = None,
                   properties: dict = None, free_properties: dict = None, labels: list = None):
    data = dict(local_id=local_id,
                entity_type=entity_type,
                entity_name=entity_name,
                properties=properties,
                free_properties=free_properties,
                labels=labels)
    resp = requests.post('{}/entities'.format(base_url), json=data)
    assert resp.status_code == 200, resp.text


def _get_entity(id: str = None, local_id: str = None):
    url = '{}/entities/{}'.format(base_url, quote(id or local_id))
    if id:
        resp = requests.get(url)
    else:
        resp = requests.get('{}?by_local=1'.format(url))
    assert resp.status_code == 200, resp.text
    return resp.json()


def _delete_entity(id: str = None, local_id: str = None):
    url = '{}/entities/{}'.format(base_url, quote(id or local_id))
    if id:
        resp = requests.delete(url)
    else:
        resp = requests.delete('{}?by_local=1'.format(url))
    assert resp.status_code == 200, resp.text


def _create_relation(head_entity_id: str = None, relation_type: str = None, tail_entity_id: str = None,
                     by_local: bool = False):
    url = '{}/relations'.format(base_url)
    if by_local:
        url += '?by_local=1'
    data = {
        'head_entity_id': head_entity_id,
        'tail_entity_id': tail_entity_id,
        'relation_type': relation_type
    }
    resp = requests.post(url, json=data)
    assert resp.status_code == 200, resp.text


def _delete_relation(head_entity_id: str = None, relation_type: str = None, tail_entity_id: str = None,
                     by_local: bool = False):
    url = '{}/relations/delete'.format(base_url)
    if by_local:
        url += '?by_local=1'
    data = {
        'head_entity_id': head_entity_id,
        'tail_entity_id': tail_entity_id,
        'relation_type': relation_type
    }
    resp = requests.post(url, json=data)
    assert resp.status_code == 200, resp.text


def _delete_entity_relations(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/relations'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.delete(url)
    assert resp.status_code == 200, resp.text


def _find_parents(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-parents'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()


def _find_children(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-children'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()


def _find_neighbors(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-neighbors'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()
