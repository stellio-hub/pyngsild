from property import Property


class Entity():
    '''
    The Entity class represent an Entity object as defined by the NGSI-LD
    information model

    Parameters:
    -----------
    id: URI
        Identifier of the entity

    type: str
        Shall be the Entity Type Name

    properties: Property
        One or more Property object

    Return:
    -------
    Entity: an instance of this class
    '''
    def __init__(self, id, type, properties=None):
        self.id = id
        self.type = type
        if properties is not None:
            self.properties = properties
        else:
            self.properties = None
        self.at_context = None

    # Object representation
    def __repr__(self):
        return(f'Class(id=\'{self.id}\', type=\'{self.type}\')')

    # id attribute
    @property
    def id(self):
        return(self._id)

    @id.setter
    def id(self, id):
        self._id = id

    # type attribute
    @property
    def type(self):
        return(self._type)

    @type.setter
    def type(self, type):
        self._type = type

    # context attribute
    @property
    def at_context(self):
        return(self._at_context)

    @at_context.setter
    def at_context(self, at_context):
        self._at_context = at_context

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
        if isinstance(properties, Property):
            self._properties = [properties]
        elif isinstance(properties, list):
            if not any(not isinstance(p, Property) for p in properties):
                self._properties = properties

    def add_properties(self, properties):
        '''
        Add property/properties to this instance of Entity. The property/ies
        are 'simply' added to the existing properties (if any). property/ies
        could be complex property/ies (i.e. a property/ies having property/ies)

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
        # when Entity does not already have any property, the Property
        # is added as a list. That will makes future addition of
        # property/ies easier (i.e. the property is appended)
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

    def to_ngsild(self):
        '''
        Generate a NGSI-LD compliant representation of this instance of
        Entity. It includes all properties/sub-properties (and recursively,
        sub-properties of sub-properties, etc.) and @Context.

        Parameters:
        -----------
        None

        Return:
        -------
        ngsild: Dictionary
            NGSI-LD compliant representation of this Entity
        '''
        ngsild = {
            '@context': self.context,
            'id': self.id,
            'type': self.type
        }

        if self.properties is not None:
            p_dict = {}
            for property_ in self.properties:
                p_dict.update(property_.to_ngsild())
            ngsild.update(p_dict)

        return(ngsild)
