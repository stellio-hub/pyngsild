from pyngsild.property import Property
from pyngsild.relationship import Relationship
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
PROP_1 = Property(name='plant_health', value=5,
                  observed_at=OBSERVED_AT)
PROP_2 = Property(name='temperature', value=37,
                  observed_at=OBSERVED_AT, unit_code='CEL')
PROP_3 = Property(name='pH', value=7.3, observed_at=OBSERVED_AT,
                  unit_code='C62')

# GLOBALS for Relationship tests
R_NAME = 'to_object_1'
R_OBJECT = 'uri:object_1'
R_DATASETID = 'r:dataset:1'
