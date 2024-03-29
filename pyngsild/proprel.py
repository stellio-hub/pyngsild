'''This module define the Property, GeoProperty and Relationship class.

The Property class allows to create an NGSI-LD property. As per NGSI-LD
specification, a property could itself contains one or more properties.

    Typical usage examples:

    prop1 = Property(name='uv_index', value=10)
    prop2 = Property(name='temperature', value=15, unitCode='CEL')

The GeoProperty is a specific type of property, i.e. a Geospatial property,
that is having a value being a GeoJSON Geometry.
A GeoProperty is deemed 'final', i.e. it cannot contains other properties.
Similarly, it cannot contains relationships.

    Typical usage examples:

    geoprop1 = GeoProperty(name='location',
                           value={"type": "Point",
                           "coordinates": [39.2753478, 16.4077153]})

The Relationship class allows to create an NGSI-LD relationship. As per NGSI-LD
specification, similarly to Property, a relationship could itself contains one
or more relationships.

    Typical usage examples:

    rel1 = Relationship(name='hasObjectOne', object_='uri:of:ObjectOne')
'''
from tzlocal import get_localzone
from datetime import datetime


def is_dt_aware(dt):
    '''Evaluates if a datetime object is aware

    An aware datetime object can locate itself relative to other aware objects
    (such datetime object typically includes time zone information).

    A datetime object dt is aware if:
        dt.tzinfo is not None
        dt.tzinfo.utcoffset(dt) does not return None

    Args:
    -----
    dt: datetime
        the datetime object for which to test awareness

    Return:
    -------
    False: The datetime object is not aware
    True : The datetime object is aware
    '''
    if dt.tzinfo is not None:
        if dt.tzinfo.utcoffset(dt) is not None:
            return(True)
    return(False)


def as_isoformat(dt):
    '''Transforms a datetime object into a string

    When the datetime object is aware, a direct transformation to a string in
    isoformat is performed.

    When a datetime object is naive, the local zone (of the system running the
    pyngsild package!) is retrieved, the datetime object is then transformed to
    an aware datetime object using this local zone, and finally transformed to
    a string in isoformat.

        As an example a datetime object:

            datetime.datetime(2021, 7, 21, 13, 23, 54, 78099,
                              tzinfo=datetime.timezone.utc)

        Will be transformed into the string:

            '2021-07-21T13:23:54.078099+00:00'

    Args:
    -----
    dt: datetime
        the datetime object to transform into isoformat

    Return:
    -------
    str_dt: str
        the datetime object transformed an isoformatted string
    '''
    if is_dt_aware(dt):
        # This datetime object is Aware
        str_dt = dt.isoformat()
    else:
        # This datetime object is Naive
        local_tz = get_localzone()
        local_dt = local_tz.localize(dt)
        str_dt = local_dt.isoformat()
    return(str_dt)


class BaseProperty():
    ''' Abstract class for Property and GeoProperty classes

    Both Property and GeoProperty will be instance of BaseProperty,
    facilitating addition of properties to a property, entity or relationship.

    Args:
    -----
    name: str
        Name of the property

    observed_at (optional): str, datetime object
        DateTime of the observation of the property either as str encoded using
        ISO 8601 'Extended Format', or as a datetime object
        When a datetime object is used, if the datetime object is naive (i.e.
        does not have timezone information), the system local timezone
        is used to construct an aware datetime object.
        Datetime objects are then transformed into a str, before being assigned
        to the observed_at attribute

    datasetid (optional): URI
        Identify an instance of a property

    Return:
    -------
    BaseProperty: an instance of this class

    Raise:
    ------
    TypeError
    '''
    def __init__(self, name, observed_at=None, datasetid=None):
        self._name = name
        # calling observed_at setter from __init__
        self._observed_at = self.observed_at = observed_at
        self._datasetid = datasetid

    # name attribute
    @property
    def name(self):
        return(self._name)

    @name.setter
    def name(self, name):
        self._name = name

    # observed_at attribute
    @property
    def observed_at(self):
        return(self._observed_at)

    @observed_at.setter
    def observed_at(self, observed_at):
        if observed_at is None:
            self._observed_at = None
        elif isinstance(observed_at, datetime):
            self._observed_at = as_isoformat(observed_at)
        elif isinstance(observed_at, str):
            self._observed_at = observed_at
        else:
            raise TypeError(
                'observed_at is expecting to be of type datetime or str')

    # datasetid attribute
    @property
    def datasetid(self):
        return(self._datasetid)

    @datasetid.setter
    def datasetid(self, datasetid):
        self._datasetid = datasetid


class GeoProperty(BaseProperty):
    '''
    The GeoProperty class represent a Geospatial property object as defined by
    the NGSI-LD information model.
    A GeoProperty is considered 'final', i.e. no property or relationship can
    be added to a GeoProperty.

    Parameters:
    -----------
    name: str
        Name of the property

    value: dict
        A dictionnary containing the type of GeoJSON geometry which is made up
        of a type (e.g. Point, LineString, etc.) and of coordinates.

    observed_at (optional): str, datetime object
        DateTime of the observation of the property either as str encoded using
        ISO 8601 'Extended Format', or as a datetime object
        When a datetime object is used, if the datetime object is naive (i.e.
        does not have timezone information), the system local timezone
        is used to construct an aware datetime object.
        Datetime objects are then transformed into a str, before being assigned
        to the observed_at attribute

    datasetid (optional): URI
        Identify an instance of a property

    Return:
    -------
    GeoProperty: an instance of this class

    Raise:
    ------
    TypeError
    '''
    def __init__(self, name, value, observed_at=None, datasetid=None):
        super().__init__(name=name, observed_at=observed_at,
                         datasetid=datasetid)
        # calling value at setter from __init__
        self._value = self.value = value

    # Object representation
    def __repr__(self):
        return(f'GeoProperty(name=\'{self.name}\', value=\'{self.value}\')')

    # value attribute
    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value):
        if isinstance(value, dict):
            self._value = value
        else:
            raise TypeError(
                '\'value\' is expected to be of type Dictionary' +
                ' as a GeoJSON geometry'
                )

    def to_ngsild(self):
        '''
        Generate a NGSI-LD compliant representation of this instance of
        GeoProperty.

        Parameters:
        -----------
        None

        Return:
        -------
        ngsild: Dictionary
            NGSI-LD compliant representation of this GeoProperty
        '''
        ngsild = {
            self._name: {
                'type': 'GeoProperty',
                'value': self._value
            }
        }
        if self._observed_at is not None:
            ngsild[self._name]['observedAt'] = self._observed_at
        if self._datasetid is not None:
            ngsild[self._name]['datasetId'] = self._datasetid

        return(ngsild)


class Property(BaseProperty):
    '''
    The Property class represent a Property object as defined by the NGSI-LD
    information model

    Args:
    -----
    name: str
        Name of the property

    value: str, numbers
        Value of the property

    observed_at (optional): str, datetime object
        DateTime of the observation of the property either as str encoded using
        ISO 8601 'Extended Format', or as a datetime object
        When a datetime object is used, if the datetime object is naive (i.e.
        does not have timezone information), the system local timezone
        is used to construct an aware datetime object.
        Datetime objects are then transformed into a str, before being assigned
        to the observed_at attribute

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

    Raise:
    ------
    TypeError
    '''
    def __init__(self, name, value, observed_at=None, unit_code=None,
                 datasetid=None, properties=None, relationships=None):
        super().__init__(name=name, observed_at=observed_at,
                         datasetid=datasetid)
        self._value = value
        self._unit_code = unit_code
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

    # value attribute
    @property
    def value(self):
        return(self._value)

    @value.setter
    def value(self, value):
        self._value = value

    # unit_code attribute
    @property
    def unit_code(self):
        return(self._unit_code)

    @unit_code.setter
    def unit_code(self, unit_code):
        self._unit_code = unit_code

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
        elif isinstance(properties, BaseProperty):
            self._properties = [properties]
        elif isinstance(properties, list):
            if not any(not isinstance(p, BaseProperty) for p in properties):
                self._properties = properties
        else:
            raise TypeError(
                '\'properties\' is expected to be of type Property' +
                ' or GeoProperty, or a List of type Property or GeoProperty'
                )

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
        elif isinstance(relationships, Relationship):
            self._relationships = [relationships]
        elif isinstance(relationships, list):
            if not any(not isinstance(r, Relationship)
                       for r in relationships):
                self._relationships = relationships
        else:
            raise TypeError(
                '\'relationships\' is expected to be of type Relationship'
                )

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
        elif isinstance(properties, BaseProperty):
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
            if not any(not isinstance(p, BaseProperty) for p in properties):
                if self._properties is None:
                    self._properties = properties
                else:
                    for property_ in properties:
                        self._properties.append(property_)
        else:
            raise TypeError(
                '\'properties\' is expected to be of type Property' +
                ' or GeoProperty, or a List of type Property or GeoProperty'
                )

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
        elif isinstance(relationships, Relationship):
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
            if not any(not isinstance(r, Relationship)
                       for r in relationships):
                if self._relationships is None:
                    self._relationships = relationships
                else:
                    for relationship in relationships:
                        self._relationships.append(relationship)
        else:
            raise TypeError(
                '\'relationships\' is expected to be of type Relationship'
                )

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
            ngsild[self._name]['observedAt'] = self._observed_at
        if self._unit_code is not None:
            ngsild[self._name]['unitCode'] = self._unit_code
        if self._datasetid is not None:
            ngsild[self._name]['datasetId'] = self._datasetid

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


class Relationship():
    '''
    The Relationship class represent a Relationship object as defined by the
    NGSI-LD information model

    Parameters:
    -----------
    name: str
        Name of the relationship

    object_: URI
        The target object of the relationship

    observed_at (optional): str, datetime object
        DateTime of the observation of the relationship either as str encoded
        using ISO 8601 'Extended Format', or as a datetime object
        When a datetime object is used, if the datetime object is naive (i.e.
        does not have timezone information), the system local timezone
        is used to construct an aware datetime object.
        Datetime objects are then transformed into a str, before being assigned
        to the observed_at attribute

    datasetid (optional): URI
        Identify an instance of a relationship

    properties (optional): Property
        One or more Property objects, the properties of the relationship

    relationships (optional): Relationship
        One or more Relationship objects, the relationship(s) of this
        relationship instance

    Return:
    -------
    Relationship: an instance of this class
    '''
    def __init__(self, name, object_, observed_at=None, datasetid=None,
                 properties=None, relationships=None):
        self._name = name
        self._type = 'Relationship'
        self._object_ = object_
        # calling observed_at setter from __init__
        self._observed_at = self.observed_at = observed_at
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
        return(f'Relationship(name=\'{self.name}' +
               f'\', object_=\'{self.object_}\')')

    # name attribute
    @property
    def name(self):
        return(self._name)

    @name.setter
    def name(self, name):
        self._name = name

    # object_ attribute
    @property
    def object_(self):
        return(self._object_)

    @object_.setter
    def object_(self, object_):
        self._object_ = object_

    # observed_at attribute
    @property
    def observed_at(self):
        return(self._observed_at)

    @observed_at.setter
    def observed_at(self, observed_at):
        if observed_at is None:
            self._observed_at = None
        elif isinstance(observed_at, datetime):
            self._observed_at = as_isoformat(observed_at)
        elif isinstance(observed_at, str):
            self._observed_at = observed_at
        else:
            raise TypeError(
                'observed_at is expecting to be of type datetime or str')

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
        elif isinstance(properties, BaseProperty):
            self._properties = [properties]
        elif isinstance(properties, list):
            if not any(not isinstance(p, BaseProperty) for p in properties):
                self._properties = properties
        else:
            raise TypeError(
                '\'properties\' is expected to be of type Property' +
                ' or GeoProperty, or a List of type Property or GeoProperty'
                )

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
        elif isinstance(relationships, Relationship):
            self._relationships = [relationships]
        elif isinstance(relationships, list):
            if not any(not isinstance(r, Relationship) for r in relationships):
                self._relationships = relationships
        else:
            raise TypeError(
                '\'relationships\' is expected to be of type Relationship'
                )

    # Add property(ies) to this instance of Relationship
    def add_properties(self, properties):
        '''
        Add property/properties to this instance of Relationship.
        The property/ies are 'simply' added to the existing properties
        (if any). property/ies could be complex property/ies (i.e. a
        property/ies having property/ies)

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
        elif isinstance(properties, BaseProperty):
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
            if not any(not isinstance(p, BaseProperty) for p in properties):
                if self._properties is None:
                    self._properties = properties
                else:
                    for property_ in properties:
                        self._properties.append(property_)
        else:
            raise TypeError(
                '\'properties\' is expected to be of type Property' +
                ' or GeoProperty, or a List of type Property or GeoProperty'
                )

    # Add relationship(s) to this instance of Relationship
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
        elif isinstance(relationships, Relationship):
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
            if not any(not isinstance(r, Relationship) for r in relationships):
                if self._relationships is None:
                    self._relationships = relationships
                else:
                    for relationship in relationships:
                        self._relationships.append(relationship)
        else:
            raise TypeError(
                '\'relationships\' is expected to be of type Relationship'
                )

    def to_ngsild(self):
        '''
        Generate a NGSI-LD compliant representation of this instance of
        Relationship. It includes all sub-relationships (and recursively,
        sub-relationships of sub-relationships, etc.) and all properties
        (and recursively, sub-properties of sub-properties, etc.)

        Parameters:
        -----------
        None

        Return:
        -------
        ngsild: Dictionary
            NGSI-LD compliant representation of this Relationship
        '''
        ngsild = {
            self._name: {
                'type': 'Relationship',
                'object': self._object_
            }
        }
        if self._observed_at is not None:
            ngsild[self._name]['observedAt'] = self._observed_at
        if self._datasetid is not None:
            ngsild[self._name]['datasetId'] = self._datasetid

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
