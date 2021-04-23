from pyngsild.proprel import Property
from . import global_test_vars as g


# Some utilities functions
def get_a_property():
    return(Property(name='plant_health',
                    value=5, observed_at=g.OBSERVED_AT))


def get_a_sub_property():
    return(Property(name='temperature',
                    value=37, observed_at=g.OBSERVED_AT, unit_code='CEL'))


# TESTS
def test_create_name_value():
    p = Property(g.P_NAME, g.P_VALUE)
    assert p.name == g.P_NAME and p.value == g.P_VALUE


def test_create_name_value_observed_at():
    p = Property(g.P_NAME, g.P_VALUE, g.OBSERVED_AT)
    assert p.name == g.P_NAME and p.value == g.P_VALUE \
        and p.observed_at == g.OBSERVED_AT


def test_create_name_value_observed_unit_code():
    p = Property(g.P_NAME, g.P_VALUE, g.OBSERVED_AT, g.P_UNIT_CODE)
    assert p.name == g.P_NAME and p.value == g.P_VALUE \
        and p.observed_at == g.OBSERVED_AT and p.unit_code == g.P_UNIT_CODE


def test_create_all_args():
    p = Property(g.P_NAME, g.P_VALUE, g.OBSERVED_AT,
                 g.P_UNIT_CODE, g.P_DATASETID)
    assert p.name == g.P_NAME and p.value == g.P_VALUE \
        and p.observed_at == g.OBSERVED_AT \
        and p.unit_code == g.P_UNIT_CODE and p._datasetid == g.P_DATASETID


def test_to_ngsild_one_property():
    p = g.PROP_1
    ngsild_true = {
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': g.OBSERVED_AT
        }
    }
    assert p.to_ngsild() == ngsild_true


def test_to_ngsild_one_sub_property():
    g.PROP_1.add_properties(g.PROP_2)
    ngsild_true = {
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': g.OBSERVED_AT,
            'temperature': {
                'type': 'Property',
                'value': 37,
                'observedAt': g.OBSERVED_AT,
                'unitCode': 'CEL'
            }
        }
    }
    assert g.PROP_1.to_ngsild() == ngsild_true
