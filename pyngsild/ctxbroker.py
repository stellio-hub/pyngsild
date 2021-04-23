import requests
from pyngsild.entity import Entity
from pyngsild.proprel import Property

URL_ENTITIES = 'ngsi-ld/v1/entities/'


class ContextBroker():
    '''
    The ContextBroker class represents a connection to a NGSI-LD Context Broker

    Parameters:
    -----------
    cb_host: HTTP URL
        Hostname of the Context Broker, e.g.: http://myctxbroker.com/

    auth_token: str
        authorisation token for connecting to the Context Broker

    Return:
    -------
    ContextBroker: an instance of a Context Broker
    '''

    def __init__(self, cb_host, auth_token):
        self._cb_host = cb_host
        self._auth_token = auth_token
        self.post_headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'Content-Type': 'application/ld+json'
        }
        self.get_headers = {
            'Authorization': 'Bearer ' + self.auth_token,
            'Content-Type': 'application/ld+json'
        }

    # Object representation
    def __repr__(self):
        return(f'ContextBroker(cb_host=\'{self.cb_host}' +
               f'\', auth_token=\'{self.auth_token}\')')

    # cb_host attribute
    @property
    def cb_host(self):
        return(self._cb_host)

    @cb_host.setter
    def cb_host(self, cb_host):
        self._cb_host = cb_host

    # auth_token attribute
    @property
    def auth_token(self):
        return(self._auth_token)

    @auth_token.setter
    def auth_token(self, auth_token):
        self._auth_token = auth_token

    def query_entities(self, query_params):
        '''
        Query entities from the Context Broker

        Parameters:
        -----------
        query_params: dict
            Query parameters

        Return:
        -------
        r: requests.models.Response
            the response from the Context Broker.
            if the request is successful, entities are accessible as JSON at r.json()
        '''
        url = self.cb_host + URL_ENTITIES
        r = requests.get(url, headers=self.get_headers, params=query_params)
        return(r)

    def get_entity(self, id):
        '''
        Get an entity by id from the Context Broker

        Parameters:
        -----------
        id: URI
            Identifier of the entity

        Return:
        -------
        r: requests.models.Response
            the response from the Context Broker. if the request is successful,
            the entity is accessible as JSON at r.json()
        '''
        url = self.cb_host + URL_ENTITIES + id
        r = requests.get(url, headers=self.get_headers)
        return(r)

    def create_entity(self, entity):
        '''
        Create an entity by id into the Context Broker

        Parameters:
        -----------
        entity: Entity
            An instance of Entity

        Return:
        -------
        r: requests.models.Response

        Raise:
        ------
        TypeError
        '''
        if not isinstance(entity, Entity):
            raise TypeError
        else:
            url = self.cb_host + URL_ENTITIES
            ngsild = entity.to_ngsild()
            r = requests.post(url, json=ngsild, headers=self.post_headers)
        return(r)

    def update_property(self, entity, property_):
        '''
        Update a property of an entity into the Context Broker

        Parameters:
        -----------
        entity: Entity
            An instance of Entity, the entity for which the property will be
            updated

        property_: Property
            An instance of Property, the property to update

        Return:
        -------
        r: requests.models.Response

        Raise:
        ------
        TypeError
        '''
        if not isinstance(entity, Entity):
            raise TypeError
        if not isinstance(property_, Property):
            raise TypeError
        else:
            url = self.cb_host + URL_ENTITIES + entity.id + '/attrs'
            ngsild = property_.to_ngsild()
            ngsild['@context'] = entity.at_context
            r = requests.patch(url, json=ngsild, headers=self.post_headers)
        return(r)

    def delete_entity(self, entity_id):
        '''
        Delete an entity by id from the Context Broker

        Parameters:
        -----------
        entity_id: URI
            The unique identifier of the entity

        Return:
        -------
        r: requests.models.Response
        '''
        url = self.cb_host + URL_ENTITIES + entity_id
        r = requests.delete(url, headers=self.get_headers)
        return(r)
