# coding=utf-8

from urllib.parse import quote

import requests

base_url = 'http://localhost:6660/api'


def create_entity(local_id: str = None, entity_type: str = None, entity_name: str = None,
                   properties: dict = None, free_properties: dict = None, labels: list = None):
    data = dict(local_id=local_id,
                entity_type=entity_type,
                entity_name=entity_name,
                properties=properties,
                free_properties=free_properties,
                labels=labels)
    resp = requests.post('{}/entities'.format(base_url), json=data)
    assert resp.status_code == 200, resp.text


def create_entities(local_id: str = None, entity_type: str = None, entity_name: str = None,
                     properties: dict = None, free_properties: dict = None, labels: list = None, n=2):
    data = []
    for i in range(n):
        d = dict(local_id='{}{}'.format(local_id, i + 1),
                 entity_type=entity_type,
                 entity_name=entity_name,
                 properties=properties,
                 free_properties=free_properties,
                 labels=labels)
        data.append(d)
    resp = requests.post('{}/_bulk/entities'.format(base_url), json=data)
    assert resp.status_code == 200, resp.text


def get_entity(id: str = None, local_id: str = None):
    url = '{}/entities/{}'.format(base_url, quote(id or local_id))
    if id:
        resp = requests.get(url)
    else:
        resp = requests.get('{}?by_local=1'.format(url))
    assert resp.status_code == 200, resp.text
    return resp.json()


def delete_entity(id: str = None, local_id: str = None):
    url = '{}/entities/{}'.format(base_url, quote(id or local_id))
    if id:
        resp = requests.delete(url)
    else:
        resp = requests.delete('{}?by_local=1'.format(url))
    assert resp.status_code == 200, resp.text


def create_relation(head_entity_id: str = None, relation_type: str = None, tail_entity_id: str = None,
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


def delete_relation(head_entity_id: str = None, relation_type: str = None, tail_entity_id: str = None,
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


def delete_entity_relations(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/relations'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.delete(url)
    assert resp.status_code == 200, resp.text


def find_parents(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-parents'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()


def find_children(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-children'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()


def find_neighbors(entity_id: str = None, by_local: bool = False):
    url = '{}/entities/{}/find-neighbors'.format(base_url, quote(entity_id))
    if by_local:
        url += '?by_local=1'
    resp = requests.post(url)
    assert resp.status_code == 200, resp.text
    return resp.json()
