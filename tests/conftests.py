from pyngsild.entity import Entity
from pyngsild.proprel import Property
from pyngsild.proprel import Relationship
from datetime import datetime, timezone
import pytz


timezone_France = pytz.timezone('Europe/Paris')


class ConfTests():
    '''
    ConfTests contains some configuration for the tests, e.g. values to
    create an instance of class entity, property, etc.
    '''
    def __init__(self):
        self._AT_CONTEXT = [
            'https://raw.githubusercontent.com/dummy/ngsild-api-data-models/'
            'main/jsonld-contexts/mydummy-contexts.jsonld'
        ]
        self._AT_CONTEXT_LINK = '<https://raw.githubusercontent.com/senseen/'\
            'ngsild-api-data-models/main/scanner/jsonld-contexts/'\
            'scanSmartMeter-compound.jsonld>; '\
            'rel=http://www.w3.org/ns/json-ld#context; type=application/json'
        self._OBSERVED_AT =\
            timezone_France.localize(datetime.now()).isoformat()
        self.NAIVE_DATETIME =\
            datetime(2021, 7, 22, 10, 11, 12, 13, tzinfo=None)
        self.NAIVE_DATETIME_STR = '2021-07-22T10:11:12.000013+02:00'
        self.AWARE_DATETIME =\
            datetime(2021, 7, 22, 10, 11, 12, 13, tzinfo=timezone.utc)
        self.AWARE_DATETIME_STR = '2021-07-22T10:11:12.000013+00:00'
        self._E_ID = 'uri:entity:1'
        self._E_TYPE = 'ENTITY'
        self._P_NAME = 'a_property'
        self._P_VALUE = 17
        self._P_UNIT_CODE = 'SEC'
        self._P_DATASETID = 'urn:p_datasetid:1'
        self._R_NAME = 'to_object_1'
        self._R_OBJECT = 'uri:object_1'
        self._R_DATASETID = 'r:dataset:1'

    @property
    def AT_CONTEXT(self):
        return(self._AT_CONTEXT)

    @property
    def AT_CONTEXT_LINK(self):
        return(self._AT_CONTEXT_LINK)

    @property
    def OBSERVED_AT(self):
        return(self._OBSERVED_AT)

    @property
    def E_ID(self):
        return(self._E_ID)

    @property
    def E_TYPE(self):
        return(self._E_TYPE)

    @property
    def P_NAME(self):
        return(self._P_NAME)

    @property
    def P_VALUE(self):
        return(self._P_VALUE)

    @property
    def P_UNIT_CODE(self):
        return(self._P_UNIT_CODE)

    @property
    def P_DATASETID(self):
        return(self._P_DATASETID)

    @property
    def R_NAME(self):
        return(self._R_NAME)

    @property
    def R_OBJECT(self):
        return(self._R_OBJECT)

    @property
    def R_DATASETID(self):
        return(self._R_DATASETID)

    def ent_1(self):
        e = Entity(id=self._E_ID, type=self._E_TYPE)
        return(e)

    def prop_1(self):
        p = Property(name='plant_health', value=5,
                     observed_at=self._OBSERVED_AT)
        return(p)

    def prop_2(self):
        p = Property(name='temperature', value=37,
                     observed_at=self._OBSERVED_AT, unit_code='CEL')
        return(p)

    def prop_3(self):
        p = Property(name='pH', value=7.3, observed_at=self._OBSERVED_AT,
                     unit_code='C62')
        return(p)

    def rel_1(self):
        r = Relationship(name=self._R_NAME, object_=self._R_OBJECT,
                         observed_at=self._OBSERVED_AT)
        return(r)

    def rel_2(self):
        r = Relationship(name='to_object_2', object_='uri:object_2',
                         observed_at=self._OBSERVED_AT,
                         datasetid='r:dataset:2')
        return(r)
