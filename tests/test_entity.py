from pyngsild.entity import Entity
from pyngsild.property import Property
from datetime import datetime
import pytz

timezone_France = pytz.timezone('Europe/Paris')

ID = 'uri:myentity:1'
TYPE = 'MY_ENTITY'

AT_CONTEXT = [
    'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
    'main/jsonld-contexts/mydummy-contexts.jsonld'
]
AT_CONTEXT_LINK = '<https://raw.githubusercontent.com/senseen/'\
    'ngsild-api-data-models/main/scanner/jsonld-contexts/'\
    'scanSmartMeter-compound.jsonld>; '\
    'rel=http://www.w3.org/ns/json-ld#context; type=application/json'

PROP_OBSERVED_AT = timezone_France.localize(datetime.now()).isoformat()
PROP_1 = Property(name='plant_health', value=5,
                  observed_at=PROP_OBSERVED_AT)
PROP_2 = Property(name='temperature', value=37,
                  observed_at=PROP_OBSERVED_AT, unit_code='CEL')
PROP_3 = Property(name='pH', value=7.3, observed_at=PROP_OBSERVED_AT,
                  unit_code='C62')


# Some utilities functions
def get_an_entity():
    e = Entity(id=ID, type=TYPE)
    return(e)


def get_an_entity_with_context():
    e = get_an_entity()
    e.at_context = AT_CONTEXT
    return(e)


# TESTS
def test_create_id_type():
    e = Entity(ID, TYPE)
    assert e.id == ID and e.type == TYPE


def test_set_context():
    e = Entity(ID, TYPE)
    e.at_context = AT_CONTEXT
    assert e.at_context == AT_CONTEXT


def test_set_one_property():
    e = get_an_entity()
    e.properties = PROP_1
    # when set, a single property is set as a  list
    # hence assertion to [PROP_1]
    assert e.properties == [PROP_1]


def test_add_first_property():
    e = get_an_entity()
    e.add_properties(PROP_1)
    # when added, a single property is added as a list
    # hence assertion to [PROP_1]
    assert e.properties == [PROP_1]


def test_add_another_property():
    e = get_an_entity()
    e.add_properties(PROP_1)
    e.add_properties(PROP_2)
    assert e.properties == [PROP_1, PROP_2]


def test_add_list_of_properties():
    e = get_an_entity()
    e.add_properties([PROP_1, PROP_2])
    assert e.properties == [PROP_1, PROP_2]


def test_simple_entity_to_ngsild():
    e = get_an_entity()
    ngsild_true = {
        '@context': None,
        'id': 'uri:myentity:1',
        'type': 'MY_ENTITY'
    }
    assert e.to_ngsild() == ngsild_true


def test_simple_entity_with_context_to_ngsild():
    e = get_an_entity_with_context()
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:myentity:1',
        'type': 'MY_ENTITY'
    }
    assert e.to_ngsild() == ngsild_true


def test_entity_two_properties_to_nsgild():
    e = get_an_entity_with_context()
    e.add_properties([PROP_1, PROP_2])
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:myentity:1',
        'type': 'MY_ENTITY',
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': PROP_OBSERVED_AT
        },
        'temperature': {
            'type': 'Property',
            'value': 37,
            'observedAt': PROP_OBSERVED_AT,
            'unitCode': 'CEL'
        }
    }
    assert e.to_ngsild() == ngsild_true


def test_entity_one_property_one_sub_property_to_nsgild():
    e = get_an_entity_with_context()
    p = PROP_1
    p.add_properties(PROP_2)
    e.add_properties(p)
    ngsild_true = {
        '@context': [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ],
        'id': 'uri:myentity:1',
        'type': 'MY_ENTITY',
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': PROP_OBSERVED_AT,
            'temperature': {
                'type': 'Property',
                'value': 37,
                'observedAt': PROP_OBSERVED_AT,
                'unitCode': 'CEL'
            }
        }
    }
    assert e.to_ngsild() == ngsild_true
