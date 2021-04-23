from . conftests import ConfTests


conf = ConfTests()


# TESTS
def test_create_id_type():
    e = conf.ent_1()
    assert e.id == conf.E_ID and e.type == conf.E_TYPE


def test_set_context():
    e = conf.ent_1()
    e.at_context = conf.AT_CONTEXT
    assert e.at_context == conf.AT_CONTEXT


def test_set_one_property():
    e = conf.ent_1()
    p = conf.prop_1()
    e.properties = p
    # when set, a single property is set as a  list
    # hence assertion to [PROP_1]
    assert e.properties == [p]


def test_add_first_property():
    e = conf.ent_1()
    p = conf.prop_1()
    e.add_properties(p)
    # when added, a single property is added as a list
    # hence assertion to [PROP_1]
    assert e.properties == [p]


def test_add_another_property():
    e = conf.ent_1()
    p1 = conf.prop_1()
    p2 = conf.prop_2()
    e.add_properties(p1)
    e.add_properties(p2)
    assert e.properties == [p1, p2]


def test_add_list_of_properties():
    e = conf.ent_1()
    p1 = conf.prop_1()
    p2 = conf.prop_2()
    e.add_properties([p1, p2])
    assert e.properties == [p1, p2]


def test_simple_entity_to_ngsild():
    e = conf.ent_1()
    ngsild_true = {
        '@context': None,
        'id': 'uri:entity:1',
        'type': 'ENTITY'
    }
    assert e.to_ngsild() == ngsild_true


def test_simple_entity_with_context_to_ngsild():
    e = conf.ent_1()
    e.at_context = conf.AT_CONTEXT
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
    e = conf.ent_1()
    e.at_context = conf.AT_CONTEXT
    e.add_properties([conf.prop_1(), conf.prop_2()])
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
            'observedAt': conf.OBSERVED_AT
        },
        'temperature': {
            'type': 'Property',
            'value': 37,
            'observedAt': conf.OBSERVED_AT,
            'unitCode': 'CEL'
        }
    }
    assert e.to_ngsild() == ngsild_true


def test_entity_one_property_one_sub_property_to_nsgild():
    e = conf.ent_1()
    e.at_context = conf.AT_CONTEXT
    p = conf.prop_1()
    p.add_properties(conf.prop_2())
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
            'observedAt': conf.OBSERVED_AT,
            'temperature': {
                'type': 'Property',
                'value': 37,
                'observedAt': conf.OBSERVED_AT,
                'unitCode': 'CEL'
            }
        }
    }
    assert e.to_ngsild() == ngsild_true
