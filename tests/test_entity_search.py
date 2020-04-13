# coding=utf-8

from tests.api import search_entities, create_entity, delete_entity


def test_entity_search():
    local_id = 'person_小明'
    name = '小明'
    entity_type = 'person'
    properties = {
        'age': 18,
        'hobbies': ['游戏', '食物']
    }
    create_entity(local_id=local_id, entity_type=entity_type, entity_name=name,
                  properties=properties)

    result = search_entities('学习')
    assert len(result) == 0
    result = search_entities('游戏')
    assert len(result) == 1
    assert result[0]['local_id'] == local_id
    result = search_entities('小明')
    assert len(result) == 1
    assert result[0]['local_id'] == local_id

    delete_entity(local_id=local_id)
