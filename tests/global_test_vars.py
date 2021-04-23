from pyngsild.proprel import Property
from pyngsild.proprel import Relationship
from datetime import datetime
import pytz

timezone_France = pytz.timezone('Europe/Paris')
OBSERVED_AT = timezone_France.localize(datetime.now()).isoformat()

# CONTEXT
AT_CONTEXT = [
    'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
    'main/jsonld-contexts/mydummy-contexts.jsonld'
]
AT_CONTEXT_LINK = '<https://raw.githubusercontent.com/senseen/'\
    'ngsild-api-data-models/main/scanner/jsonld-contexts/'\
    'scanSmartMeter-compound.jsonld>; '\
    'rel=http://www.w3.org/ns/json-ld#context; type=application/json'

# GLOBALS for Entity Class tests
E_ID = 'uri:entity:1'
E_TYPE = 'ENTITY'

# GLOBALS for Property Class tests
P_NAME = 'a_property'
P_VALUE = 17
P_UNIT_CODE = 'SEC'
P_DATASETID = 'urn:p_datasetid:1'

PROP_1 = Property(name='plant_health', value=5,
                  observed_at=OBSERVED_AT)
PROP_2 = Property(name='temperature', value=37,
                  observed_at=OBSERVED_AT, unit_code='CEL')
PROP_3 = Property(name='pH', value=7.3, observed_at=OBSERVED_AT,
                  unit_code='C62')

# GLOBALS for Relationship Class tests
R_NAME = 'to_object_1'
R_OBJECT = 'uri:object_1'
R_DATASETID = 'r:dataset:1'

REL_1 = Relationship(name=R_NAME, object_=R_OBJECT, observed_at=OBSERVED_AT,
                     datasetid=R_DATASETID)
REL_2 = Relationship(name='to_object_2', object_='uri:object_2',
                     observed_at=OBSERVED_AT, datasetid='r:dataset:2')
