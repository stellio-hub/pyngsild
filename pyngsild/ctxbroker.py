import requests
from pyngsild.entity import Entity
from pyngsild.proprel import Property

URL_ENTITIES = 'ngsi-ld/v1/entities/'


class ContextBroker:
    """
    The ContextBroker class represents a connection to a NGSI-LD Context Broker

    Parameters:
    -----------
    cb_host: HTTP URL
        Hostname of the Context Broker, e.g.: http://myctxbroker.com/

    Return:
    -------
    ContextBroker: an instance of a Context Broker
    """

    def __init__(self, cb_host):
        self._cb_host = cb_host

    # Object representation
    def __repr__(self):
        return f'ContextBroker(cb_host=\'{self.cb_host}\')'

    # cb_host attribute
    @property
    def cb_host(self):
        return self._cb_host

    @cb_host.setter
    def cb_host(self, cb_host):
        self._cb_host = cb_host

    def query_entities(self, request_headers, query_params):
        """
        Query entities from the Context Broker

        Parameters:
        -----------
        request_headers: dict
            Request Headers

        query_params: dict
            Query Parameters

        Return:
        -------
        response: requests.models.Response
            the response from the Context Broker.
            if the request is successful, entities are
            accessible as JSON at r.json()
        """

        response = requests.get(url=self.cb_host + URL_ENTITIES,
                                headers=request_headers, params=query_params)
        return response

    def get_entity(self, request_headers, entity_id):
        """
        Get an entity by id from the Context Broker

        Parameters:
        -----------
        request_headers: dict
            Request Headers

        entity_id: URI
            Identifier of the entity

        Return:
        -------
        response: requests.models.Response
            the response from the Context Broker. if the request is successful,
            the entity is accessible as JSON at r.json()
        """

        response = requests.get(url=self.cb_host + URL_ENTITIES + entity_id,
                                headers=request_headers)
        return response

    def create_entity(self, request_headers, entity):
        """
        Create an entity by id into the Context Broker

        Parameters:
        -----------
        request_headers: dict
            Request Headers

        entity: Entity
            An instance of Entity

        Return:
        -------
        response: requests.models.Response

        Raise:
        ------
        TypeError
        """
        if not isinstance(entity, Entity):
            raise TypeError
        else:
            ngsild_entity = entity.to_ngsild()
            response = requests.post(url=self.cb_host + URL_ENTITIES,
                                     json=ngsild_entity,
                                     headers=request_headers)
        return response

    def update_property(self, request_headers, entity, property_):
        """
        Update a property of an entity into the Context Broker

        Parameters:
        -----------
        request_headers: dict
            Request Headers

        entity: Entity
            An instance of Entity, the entity for which the property will be
            updated

        property_: Property
            An instance of Property, the property to update

        Return:
        -------
        response: requests.models.Response

        Raise:
        ------
        TypeError
        """
        if not isinstance(entity, Entity):
            raise TypeError
        if not isinstance(property_, Property):
            raise TypeError
        else:
            ngsild_property = property_.to_ngsild()
            ngsild_property['@context'] = entity.at_context
            response = requests.patch(
                url=self.cb_host + URL_ENTITIES + entity.id + '/attrs',
                json=ngsild_property,
                headers=request_headers
            )
        return response

    def delete_entity(self, request_headers, entity_id):
        """
        Delete an entity by id from the Context Broker

        Parameters:
        -----------
        request_headers: dict
            Request Headers

        entity_id: URI
            The unique identifier of the entity

        Return:
        -------
        response: requests.models.Response
        """

        response = requests.delete(url=self.cb_host + URL_ENTITIES
                                   + entity_id, headers=request_headers)
        return response
