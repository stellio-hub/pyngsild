class Property():
    '''
    The Property class represent a Property object as defined by the NGSI-LD
    information model

    Parameters:
    -----------
    name: str
        Name of the property

    value: str, numbers
        Value of the property

    observed_at: str
        DateTime of the observation of the property, as str encoded using
        ISO 8601 'Extended Format'

    unitCode: str
        Unit code of the measurement unit, encoded using the UN/CEFACT Common
        Codes for Units of Measurement

    datasetid: URI
        Instance of a property

    properties: Property
        One or more Property objects, the  property(ies) of this property
        instance

    Return:
    -------
    Property: an instance of this class
    '''
    def __init__(self, name, value, observed_at=None, unit_code=None,
                 datasetid=None, properties=None):
        self._name = name
        self._value = value
        self._observed_at = observed_at
        self._unit_code = unit_code
        self._datasetid = datasetid
        if properties is not None:
            self.add_properties(properties)
        else:
            self.properties = None

    # Object representation
    def __repr__(self):
        return(f'Property(name=\'{self.name}\', value=\'{self.value}\')')

    # name attribute
    @property
    def name(self):
        return(self._name)

    @name.setter
    def name(self, name):
        self._name = name

    # value attribute
    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    # observed_at attribute
    @property
    def observed_at(self):
        return(self._observed_at)

    @observed_at.setter
    def observed_at(self, observed_at):
        self._observed_at = observed_at

    # unit_code attribute
    @property
    def unit_code(self):
        return(self._unit_code)

    @unit_code.setter
    def unit_code(self, unit_code):
        self._unit_code = unit_code

    # datasetid attribute
    @property
    def datasetid(self):
        return(self._datasetid)

    @datasetid.setter
    def datasetid(self, datasetid):
        self._datasetid = datasetid

    def add_properties(self, properties):
        '''
        Adding property/properties to this instance of Property. A Property
        could have 1 one more properties, there are stored as a list.

        Parameters:
        -----------
        properties: None, Property or list of Property
            One or more properties

        Return:
        -------
        None

        Raise:
        ------
        TypeError
        '''
        if properties is None:
            pass
        elif isinstance(properties, Property):
            if self.properties is None:
                self.properties = [properties]
            else:
                self.properties.append(properties)
        elif isinstance(properties, list):
            if not any(not isinstance(p, Property) for p in properties):
                if self.properties is None:
                    self.properties = properties
                else:
                    for property_ in properties:
                        self.properties.append(property_)
        else:
            raise TypeError

        return

    def to_ngsild(self):
        '''
        Generate a NGSI-LD compliant representation of this instance of
        Property. It includes all sub-properties (and recursively,
        sub-properties of sub-properties, etc.)

        Parameters:
        -----------
        None

        Return:
        -------
        ngsild: Dictionary
            NGSI-LD compliant representation of this Property
        '''
        ngsild = {
            self._name: {
                'type': 'Property',
                'value': self._value
            }
        }
        if self._observed_at is not None:
            ngsild[self._name]['observedAt'] = self._observed_at
        if self._unit_code is not None:
            ngsild[self._name]['unitCode'] = self._unit_code
        if self._datasetid is not None:
            ngsild[self._name]['datasetid'] = self._datasetid

        if self.properties is not None:
            p_dict = {}
            for property_ in self.properties:
                p_dict.update(property_.to_ngsild())
            ngsild[self._name].update(p_dict)

        return(ngsild)
