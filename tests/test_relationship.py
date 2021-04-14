from pyngsild.relationship import Relationship
from . import global_test_vars as g


# TESTS
def test_create_name_object():
    r = Relationship(g.R_NAME, g.R_OBJECT)
    assert r.name == g.R_NAME and r.object_ == g.R_OBJECT


def test_create_name_object_observed_at():
    r = Relationship(g.R_NAME, g.R_OBJECT, g.OBSERVED_AT)
    assert r.name == g.R_NAME and r.object_ == g.R_OBJECT \
        and r.observed_at == g.OBSERVED_AT


def test_create_all_args():
    r = Relationship(g.R_NAME, g.R_OBJECT, g.OBSERVED_AT, g.R_DATASETID)
    assert r.name == g.R_NAME and r.object_ == g.R_OBJECT \
        and r.observed_at == g.OBSERVED_AT and r.datasetid == g.R_DATASETID


def test_to_ngsild_one_relationship():
    r = Relationship(g.R_NAME, g.R_OBJECT, g.OBSERVED_AT)
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observed_at': g.OBSERVED_AT
        }
    }
    assert r.to_ngsild() == ngsild_true


def test_to_ngsild_one_sub_relationship():
    r = Relationship(g.R_NAME, g.R_OBJECT, g.OBSERVED_AT)
    r.add_relationships(g.REL_2)
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observed_at': g.OBSERVED_AT,
            'to_object_2': {
                'type': 'Relationship',
                'object': 'uri:object_2',
                'observed_at': g.OBSERVED_AT,
                'datasetid': 'r:dataset:2'
            }
        }
    }
    assert r.to_ngsild() == ngsild_true


def test_to_ngsild_relationship_property():
    r = Relationship(g.R_NAME, g.R_OBJECT, g.OBSERVED_AT)
    r.add_properties(g.PROP_1)
    ngsild_true = {
        'to_object_1': {
            'type': 'Relationship',
            'object': 'uri:object_1',
            'observed_at': g.OBSERVED_AT,
            'to_object_2': {
                'type': 'Relationship',
                'object': 'uri:object_2',
                'observed_at': g.OBSERVED_AT,
                'datasetid': 'r:dataset:2'
            }
        }
    }
    assert r.to_ngsild() == ngsild_true
