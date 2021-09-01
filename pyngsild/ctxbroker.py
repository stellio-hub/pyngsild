import requests
from pyngsild.entity import Entity
from pyngsild.proprel import Property, Relationship
from typing import Union


URL_ENTITIES = 'ngsi-ld/v1/entities/'


class ContextBroker:
    """
    The ContextBroker class represents a connection to a NGSI-LD Context Broker

    Args:
        -----
    cb_host: HTTP URL
        Hostname of the Context Broker, e.g.: http://myctxbroker.com/

    Returns:
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

    def query_entities(self, request_headers: dict,
                       query_params: str) -> requests.models.Response:
        """Query entities from the Context Broker

        (NGSI-LD "Query Entities" operation,
         HTTP Binding: GET entities/)

        Args:
        -----
        request_headers: dict
            Request Headers

        query_params: str
            Query Parameters

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """
        response = requests.get(url=self.cb_host + URL_ENTITIES,
                                headers=request_headers, params=query_params)
        return response

    def retrieve_entity(self, request_headers: dict,
                        entity_id: str) -> requests.models.Response:
        """Retrieve an entity by id from the Context Broker

        (NGSI-LD "Retrieve Entity" operation,
         HTTP Binding: GET entities/{entityId})

        Args:
        -----
        request_headers: dict
            Request Headers

        entity_id: URI
            Identifier of the entity

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """
        response = requests.get(url=self.cb_host + URL_ENTITIES + entity_id,
                                headers=request_headers)
        return response

    def create_entity(self, request_headers: dict,
                      entity: Entity) -> requests.models.Response:
        """Create an entity into the Context Broker

        (NGSI-LD "Create Entity" operation,
         HTTP Binding: POST entities/)

        Args:
        -----
        request_headers: dict
            Request Headers

        entity: Entity
            An instance of Entity

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()

        Raises:
        ------
        TypeError
        """
        if not isinstance(entity, Entity):
            raise TypeError('entity must be of type \'Entity\'')
        else:
            ngsild_entity = entity.to_ngsild()
            response = requests.post(url=self.cb_host + URL_ENTITIES,
                                     json=ngsild_entity,
                                     headers=request_headers)
        return response

    def update_entity_attributes(self, request_headers: dict,
                                 entity_id: str,
                                 at_context: str,
                                 fragment: Union[Property, Relationship])\
                                 -> requests.models.Response:
        """Update entity attributes into the Context Broker

        An entity attributes can be a Property or Relationship

        (NGSI-LD "Update Entity Attributes" operation,
         HTTP Binding: PATCH entities/{entityId}/attrs/)

        Args:
        -----
        request_headers: A Request Headers
        entity_id: URN of the entity for which the fragment will be updated
        at_context: The context information
        fragment: The entity's fragment to update as a Property/Relationship
            instance 

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()

        Raises:
        ------
        TypeError
        """
        if not (isinstance(fragment, Property) 
                or isinstance(fragment, Relationship)):
            raise TypeError('fragment must be of type \'Property\''+
                            'or \'Relationship\'')
        else:
            ngsild_fragment = fragment.to_ngsild()
            ngsild_fragment['@context'] = at_context
            response = requests.patch(
                url=self.cb_host + URL_ENTITIES + entity_id + '/attrs/',
                json=ngsild_fragment,
                headers=request_headers
            )
        return response

    def append_entity_attributes(self, request_headers: dict,
                                 entity_id: str,
                                 at_context: str,
                                 fragment: Union[Property, Relationship])\
                                 -> requests.models.Response:
        """Append attributes to an entity into the Context Broker

        An entity attributes can be a Property or Relationship

        (NGSI-LD "Append Entity Attributes" operation,
         HTTP Binding: POST entities/{entityId}/attrs/)

        Args:
        -----
        request_headers: A Request Headers
        entity_id: URN of the entity for which the fragment will be updated
        at_context: The context information
        fragment: The entity's fragment to update as a Property/Relationship
            instance 

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()

        Raises:
        ------
        TypeError
        """
        if not (isinstance(fragment, Property)
                or isinstance(fragment, Relationship)):
            raise TypeError('fragment must be of type \'Property\''+
                            'or \'Relationship\'')
        else:
            ngsild_fragment = fragment.to_ngsild()
            ngsild_fragment['@context'] = at_context
            response = requests.post(
                url=self.cb_host + URL_ENTITIES + entity_id + '/attrs/',
                json=ngsild_fragment,
                headers=request_headers
            )
        return response

    def delete_entity(self, request_headers: dict,
                      entity_id: str) -> requests.models.Response:
        """Delete an entity by id from the Context Broker

        (NGSI-LD "Delete Entity" operation,
         HTTP Binding: DELETE entities/{entityId})

        Args:
        -----
        request_headers: A Request Headers
        entity_id: The unique identifier of the entity

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """

        response = requests.delete(url=self.cb_host + URL_ENTITIES
                                   + entity_id, headers=request_headers)
        return response
