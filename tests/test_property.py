from pyngsild.property import Property
from datetime import datetime
import pytz

timezone_France = pytz.timezone('Europe/Paris')
PROP_NAME = 'myproperty'
PROP_VALUE = 17
PROP_OBSERVED_AT = timezone_France.localize(datetime.now()).isoformat()
PROP_UNIT_CODE = 'SEC'
PROP_DATASETID = 'urn:mydatasetid:1'


# Some utilities functions
def get_a_property():
    return(Property(name='plant_health',
                    value=5, observed_at=PROP_OBSERVED_AT))


def get_a_sub_property():
    return(Property(name='temperature',
                    value=37, observed_at=PROP_OBSERVED_AT, unit_code='CEL'))


# TESTS
def test_create_name_value():
    p = Property(PROP_NAME, PROP_VALUE)
    assert p.name == PROP_NAME and p.value == PROP_VALUE


def test_create_name_value_observed_at():
    p = Property(PROP_NAME, PROP_VALUE, PROP_OBSERVED_AT)
    assert p.name == PROP_NAME and p.value == PROP_VALUE \
        and p.observed_at == PROP_OBSERVED_AT


def test_create_name_value_observed_unit_code():
    p = Property(PROP_NAME, PROP_VALUE, PROP_OBSERVED_AT, PROP_UNIT_CODE)
    assert p.name == PROP_NAME and p.value == PROP_VALUE \
        and p.observed_at == PROP_OBSERVED_AT and p.unit_code == PROP_UNIT_CODE


def test_create_all_args():
    p = Property(PROP_NAME, PROP_VALUE, PROP_OBSERVED_AT,
                 PROP_UNIT_CODE, PROP_DATASETID)
    assert p.name == PROP_NAME and p.value == PROP_VALUE \
        and p.observed_at == PROP_OBSERVED_AT \
        and p.unit_code == PROP_UNIT_CODE and p._datasetid == PROP_DATASETID


def test_to_ngsild_one_property():
    p = get_a_property()
    ngsild_true = {
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': PROP_OBSERVED_AT
        }
    }
    assert p.to_ngsild() == ngsild_true


def test_to_ngsild_one_sub_property():
    p = get_a_property()
    sub_p = get_a_sub_property()
    p.add_properties(sub_p)
    ngsild_true = {
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
    assert p.to_ngsild() == ngsild_true
