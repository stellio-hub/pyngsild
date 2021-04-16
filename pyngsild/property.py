import pyngsild.relationship


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

    observed_at (optional): str
        DateTime of the observation of the property, as str encoded using
        ISO 8601 'Extended Format'

    unitCode (optional): str
        Unit code of the measurement unit, encoded using the UN/CEFACT Common
        Codes for Units of Measurement

    datasetid (optional): URI
        Identify an instance of a property

    properties (optional): Property
        One or more Property objects, the  property(ies) of this property
        instance

    Return:
    -------
    Property: an instance of this class
    '''
    def __init__(self, name, value, observed_at=None, unit_code=None,
                 datasetid=None, properties=None, relationships=None):
        self._name = name
        self._value = value
        self._observed_at = observed_at
        self._unit_code = unit_code
        self._datasetid = datasetid
        if properties is not None:
            self._properties = properties
        else:
            self._properties = None
        if relationships is not None:
            self._relationships = relationships
        else:
            self._relationships = None

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

    # properties attribute
    @property
    def properties(self):
        return(self._properties)

    @properties.setter
    def properties(self, properties):
        '''
        Set (or re-set) properties. This is different from add properties
        where property(ies) could be added to existing properties.
        Here, previous properties are replaced by new properties.
        '''
        if properties is None:
            self._properties = None
        elif isinstance(properties, Property):
            self._properties = [properties]
        elif isinstance(properties, list):
            if not any(not isinstance(p, Property) for p in properties):
                self._properties = properties
        else:
            raise TypeError

    # relationships attribute
    @property
    def relationships(self):
        return(self._relationships)

    @relationships.setter
    def relationships(self, relationships):
        '''
        Set (or re-set) relationships. This is different from add relationships
        where relationship(s) could be added to existing relationships.
        Here, previous relationships are replaced by new relationships.
        '''
        if relationships is None:
            self._relationships = None
        elif isinstance(relationships, pyngsild.relationship.Relationship):
            self._relationships = [relationships]
        elif isinstance(relationships, list):
            if not any(not isinstance(r, pyngsild.relationship.Relationship)
                       for r in relationships):
                self._relationships = relationships
        else:
            raise TypeError

    # Add property(ies) to this instance of Property
    def add_properties(self, properties):
        '''
        Adding property/properties to this instance of Property. The
        property/ies are 'simply' added to the existing properties (if any).
        property/ies could be complex property/ies (i.e. a property/ies having
        property/ies)

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
        # Nothing to do if Parameters is None !
        if properties is None:
            pass

        # Parameters is a single Property:
        # when Relationship does not already have any property, the Property
        # is added as a list. That will makes future addition of property/ies
        # easier (i.e. the property is appended)
        elif isinstance(properties, Property):
            if self._properties is None:
                self._properties = [properties]
            else:
                self._properties.append(properties)

        # Parameters is a list:
        # we ensure the list is made up of only Property object.
        # When this is the case, we either SET self._properties (when
        # self._properties is None) or we add each property to the existing
        # properties.
        elif isinstance(properties, list):
            if not any(not isinstance(p, Property) for p in properties):
                if self._properties is None:
                    self._properties = properties
                else:
                    for property_ in properties:
                        self._properties.append(property_)
        else:
            raise TypeError

    # Add relationship(s) to this instance of Property
    def add_relationships(self, relationships):
        '''
        Add relationship(s) to this instance of Relationship. The
        relationship(s) are 'simply' added to the existing relationship(s)
        (if any). relationships could be complex relationships (i.e.
        a relationship(s) having relationships)

        Parameters:
        -----------
        relationships: None, Relationship or list of Relationship
            One or more relationships

        Return:
        -------
        None

        Raise:
        ------
        TypeError
        '''
        # Nothing to do if Parameters is None !
        if relationships is None:
            pass

        # Parameters is a single Relationship:
        # when Relationship does not already have any relationship, the
        # Relationship is added as a list. That will makes future addition of
        # relationship(s) easier (i.e. the relationship is appended)
        elif isinstance(relationships, pyngsild.relationship.Relationship):
            if self._relationships is None:
                self._relationships = [relationships]
            else:
                self._relationships.append(relationships)

        # Parameters is a list:
        # we ensure the list is made up of only Relationship object.
        # When this is the case, we either SET self._properties (when
        # self._properties is None) or we add each property to the existing
        # properties.
        elif isinstance(relationships, list):
            if not any(not isinstance(r, pyngsild.relationship.Relationship)
                       for r in relationships):
                if self._relationships is None:
                    self._relationships = relationships
                else:
                    for relationship in relationships:
                        self._relationships.append(relationship)
        else:
            raise TypeError

    def to_ngsild(self):
        '''
        Generate a NGSI-LD compliant representation of this instance of
        Property. It includes all sub-properties (and recursively,
        sub-properties of sub-properties, etc.) and all sub-relationships
        (and recursively, sub-relationships of sub-relationships, etc.)

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
            ngsild[self._name]['observed_at'] = self._observed_at
        if self._unit_code is not None:
            ngsild[self._name]['unitCode'] = self._unit_code
        if self._datasetid is not None:
            ngsild[self._name]['datasetid'] = self._datasetid

        if self.properties is not None:
            p_dict = {}
            for property_ in self.properties:
                p_dict.update(property_.to_ngsild())
            ngsild[self._name].update(p_dict)

        if self.relationships is not None:
            r_dict = {}
            for relationship in self.relationships:
                r_dict.update(relationship.to_ngsild())
            ngsild[self._name].update(r_dict)

        return(ngsild)
