from pyngsild.proprel import Relationship
from . conftests import ConfTests


conf = ConfTests()


# TESTS
def test_create_name_object():
    r = Relationship(conf.R_NAME, conf.R_OBJECT)
    assert r.name == conf.R_NAME and r.object_ == conf.R_OBJECT


def test_create_name_object_observed_at():
    r = Relationship(conf.R_NAME, conf.R_OBJECT, conf.OBSERVED_AT)
    assert r.name == conf.R_NAME and r.object_ == conf.R_OBJECT \
        and r.observed_at == conf.OBSERVED_AT


def test_create_all_args():
    r = Relationship(conf.R_NAME, conf.R_OBJECT, conf.OBSERVED_AT,
                     conf.R_DATASETID)
    assert r.name == conf.R_NAME and r.object_ == conf.R_OBJECT \
        and r.observed_at == conf.OBSERVED_AT \
        and r.datasetid == conf.R_DATASETID


def test_to_ngsild_one_relationship():
    r1 = conf.rel_1()
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observedAt': conf.OBSERVED_AT
        }
    }
    assert r1.to_ngsild() == ngsild_true


def test_to_ngsild_one_sub_relationship():
    r1 = conf.rel_1()
    r2 = conf.rel_2()
    r1.add_relationships(r2)
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observedAt': conf.OBSERVED_AT,
            'to_object_2': {
                'type': 'Relationship',
                'object': 'uri:object_2',
                'observedAt': conf.OBSERVED_AT,
                'datasetId': 'r:dataset:2'
            }
        }
    }
    assert r1.to_ngsild() == ngsild_true


def test_to_ngsild_relationship_property():
    r = conf.rel_1()
    p = conf.prop_1()
    r.add_properties(p)
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observedAt': conf.OBSERVED_AT,
            'plant_health': {
                'type': 'Property',
                'value': 5,
                'observedAt': conf.OBSERVED_AT
            }
        }
    }
    assert r.to_ngsild() == ngsild_true
