from pyngsild.property import Property
from datetime import datetime
import pytz

timezone_France = pytz.timezone('Europe/Paris')
PROP_NAME = 'myproperty'
PROP_VALUE = 17
PROP_OBSERVED_AT = timezone_France.localize(datetime.now()).isoformat()
PROP_UNIT_CODE = 'SEC'
PROP_DATASETID = 'urn:mydatasetid:1'


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
