from pyngsild.proprel import Property
from . conftests import ConfTests


conf = ConfTests()


# TESTS
def test_create_name_value():
    p = Property(conf.P_NAME, conf.P_VALUE)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE


def test_create_name_value_observed_at():
    p = Property(conf.P_NAME, conf.P_VALUE, conf.OBSERVED_AT)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE \
        and p.observed_at == conf.OBSERVED_AT


def test_create_name_value_observed_unit_code():
    p = Property(conf.P_NAME, conf.P_VALUE, conf.OBSERVED_AT, conf.P_UNIT_CODE)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE \
        and p.observed_at == conf.OBSERVED_AT \
        and p.unit_code == conf.P_UNIT_CODE


def test_create_all_args():
    p = Property(conf.P_NAME, conf.P_VALUE, conf.OBSERVED_AT,
                 conf.P_UNIT_CODE, conf.P_DATASETID)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE \
        and p.observed_at == conf.OBSERVED_AT \
        and p.unit_code == conf.P_UNIT_CODE \
        and p._datasetid == conf.P_DATASETID


def test_to_ngsild_one_property():
    p = conf.prop_1()
    ngsild_true = {
        'plant_health': {
            'type': 'Property',
            'value': 5,
            'observedAt': conf.OBSERVED_AT
        }
    }
    assert p.to_ngsild() == ngsild_true


def test_to_ngsild_one_sub_property():
    p = conf.prop_1()
    p.add_properties(conf.prop_2())
    ngsild_true = {
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
    assert p.to_ngsild() == ngsild_true
