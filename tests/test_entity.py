from pyngsild.entity import Entity
from . import global_test_vars as g


# Some utilities functions
def get_an_entity():
    e = Entity(id=g.E_ID, type=g.E_TYPE)
    return(e)


def get_an_entity_with_context():
    e = get_an_entity()
    e.at_context = g.AT_CONTEXT
    return(e)


# TESTS
def test_create_id_type():
    e = get_an_entity()
    assert e.id == g.E_ID and e.type == g.E_TYPE


def test_set_context():
    e = get_an_entity()
    e.at_context = g.AT_CONTEXT
    assert e.at_context == g.AT_CONTEXT


def test_set_one_property():
    e = get_an_entity()
    e.properties = g.PROP_1
    # when set, a single property is set as a  list
    # hence assertion to [PROP_1]
    assert e.properties == [g.PROP_1]


def test_add_first_property():
    e = get_an_entity()
    e.add_properties(g.PROP_1)
    # when added, a single property is added as a list
    # hence assertion to [PROP_1]
    assert e.properties == [g.PROP_1]


def test_add_another_property():
    e = get_an_entity()
    e.add_properties(g.PROP_1)
    e.add_properties(g.PROP_2)
    assert e.properties == [g.PROP_1, g.PROP_2]


def test_add_list_of_properties():
    e = get_an_entity()
    e.add_properties([g.PROP_1, g.PROP_2])
    assert e.properties == [g.PROP_1, g.PROP_2]


def test_simple_entity_to_ngsild():
    e = get_an_entity()
    ngsild_true = {
        '@context': None,
        'id': 'uri:entity:1',
        'type': 'ENTITY'
    }
    assert e.to_ngsild() == ngsild_true


def test_simple_entity_with_context_to_ngsild():
    e = get_an_entity_with_context()
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:entity:1',
        'type': 'ENTITY'
    }
    assert e.to_ngsild() == ngsild_true


def test_entity_two_properties_to_nsgild():
    e = get_an_entity_with_context()
    e.add_properties([g.PROP_1, g.PROP_2])
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:entity:1',
        'type': 'ENTITY',
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observed_at': g.OBSERVED_AT
        },
        'temperature': {
            'type': 'Property',
            'value': 37,
            'observed_at': g.OBSERVED_AT,
            'unitCode': 'CEL'
        }
    }
    assert e.to_ngsild() == ngsild_true


def test_entity_one_property_one_sub_property_to_nsgild():
    e = get_an_entity_with_context()
    p = g.PROP_1
    p.add_properties(g.PROP_2)
    e.add_properties(p)
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:entity:1',
        'type': 'ENTITY',
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observed_at': g.OBSERVED_AT,
            'temperature': {
                'type': 'Property',
                'value': 37,
                'observed_at': g.OBSERVED_AT,
                'unitCode': 'CEL'
            }
        }
    }
    assert e.to_ngsild() == ngsild_true
