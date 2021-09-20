import requests
import os
import functools
from pyngsild.entity import Entity
from pyngsild.proprel import Property, Relationship
from typing import Union, Tuple


class ContextBroker:
    """
    The ContextBroker class represents a connection to a NGSI-LD Context Broker

    Envs:
    -----
    PYNGSILD_CB_HOST: Environment variable for Context Broker host URL
        e.g. http://myctxbroker.com/
    PYNGSILD_SSO_SERVER_URL: Environment variable for the SSO server URL
    PYNGSILD_SSO_CLIENT_ID: Environment variable for the client_id
    PYNGSILD_SSO_CLIENT_SECRET = Environment variable for the client_secret

    Returns:
    --------
    ContextBroker: an instance of a Context Broker

    Raise:
    ------
    KeyError: if a required environment variable is not found
    """
    def __init__(self):
        self._cb_host = os.environ['PYNGSILD_CB_HOST']
        self._sso_server_url = os.environ['PYNGSILD_SSO_SERVER_URL']
        self._client_id = os.environ['PYNGSILD_SSO_CLIENT_ID']
        self._client_secret = os.environ['PYNGSILD_SSO_CLIENT_SECRET']
        self._URL_ENTITIES = 'ngsi-ld/v1/entities/'

        # getting the access token for accessing Context Broker
        self._access_token, self._headers = self.get_access_token()

    # Object representation
    def __repr__(self):
        return f'ContextBroker(cb_host=\'{self.cb_host}\')'

    # cb_host attribute
    @property
    def cb_host(self):
        return self._cb_host

    @property
    def access_token(self):
        return self._access_token

    @property
    def headers(self):
        return self._headers

    def get_access_token(self) -> Tuple[str, dict]:
        """ Get access token from SSO server

        Returns:
        -----
        access_token: The SSO access token
        headers: HTTP headers to be used for Context Broker operations
        """
        data = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'grant_type': 'client_credentials'
        }
        r = requests.post(
            self._sso_server_url, data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if r.status_code != 200:
            raise Exception('Cannot get Access Token.'
                            f'Status code {r.status_code}')

        access_token = r.json()['access_token']

        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/ld+json'
        }

        return(access_token, headers)

    def renew_access_token(func):
        """Renew access token on expiration

        A decorator to manage renewing the access token when
        it has expired
        """
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            r = func(self, *args, **kwargs)
            if r.status_code == 401:
                self._access_token, self._headers = self.get_access_token()
                r = func(self, *args, **kwargs)
            return r
        return wrapper

    @renew_access_token
    def query_entities(self,  query_params: str) -> requests.models.Response:
        """Query entities from the Context Broker

        (NGSI-LD "Query Entities" operation,
         HTTP Binding: GET entities/)

        Args:
        -----
        query_params: str
            Query Parameters

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """
        response = requests.get(url=self.cb_host + self._URL_ENTITIES,
                                headers=self.headers, params=query_params)
        return response

    @renew_access_token
    def retrieve_entity(self, entity_id: str) -> requests.models.Response:
        """Retrieve an entity by id from the Context Broker

        (NGSI-LD "Retrieve Entity" operation,
         HTTP Binding: GET entities/{entityId})

        Args:
        -----
        entity_id: URI
            Identifier of the entity

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """
        response = requests.get(url=self.cb_host + self._URL_ENTITIES +
                                entity_id, headers=self.headers)
        return response

    @renew_access_token
    def create_entity(self, entity: Entity) -> requests.models.Response:
        """Create an entity into the Context Broker

        (NGSI-LD "Create Entity" operation,
         HTTP Binding: POST entities/)

        Args:
        -----
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
            response = requests.post(url=self.cb_host + self._URL_ENTITIES,
                                     json=ngsild_entity,
                                     headers=self.headers)
        return response

    @renew_access_token
    def update_entity_attributes(self, entity_id: str, at_context: str,
                                 fragment: Union[Property, Relationship])\
            -> requests.models.Response:
        """Update entity attributes into the Context Broker

        An entity attributes can be a Property or Relationship

        (NGSI-LD "Update Entity Attributes" operation,
         HTTP Binding: PATCH entities/{entityId}/attrs/)

        Args:
        -----
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
            raise TypeError('fragment must be of type \'Property\'' +
                            'or \'Relationship\'')
        else:
            ngsild_fragment = fragment.to_ngsild()
            ngsild_fragment['@context'] = at_context
            response = requests.patch(
                url=self.cb_host + self._URL_ENTITIES + entity_id + '/attrs/',
                json=ngsild_fragment,
                headers=self.headers
            )
        return response

    @renew_access_token
    def append_entity_attributes(self, entity_id: str, at_context: str,
                                 fragment: Union[Property, Relationship])\
            -> requests.models.Response:
        """Append attributes to an entity into the Context Broker

        An entity attributes can be a Property or Relationship

        (NGSI-LD "Append Entity Attributes" operation,
         HTTP Binding: POST entities/{entityId}/attrs/)

        Args:
        -----
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
            raise TypeError('fragment must be of type \'Property\'' +
                            'or \'Relationship\'')
        else:
            ngsild_fragment = fragment.to_ngsild()
            ngsild_fragment['@context'] = at_context
            response = requests.post(
                url=self.cb_host + self._URL_ENTITIES + entity_id + '/attrs/',
                json=ngsild_fragment,
                headers=self.headers
            )
        return response

    @renew_access_token
    def delete_entity(self, entity_id: str) -> requests.models.Response:
        """Delete an entity by id from the Context Broker

        (NGSI-LD "Delete Entity" operation,
         HTTP Binding: DELETE entities/{entityId})

        Args:
        -----
        entity_id: The unique identifier of the entity

        Returns:
        -------
        response: HTTP status code indicating success or failure. Detailed
            errors or returned information are available as json with
            response.json()
        """

        response = requests.delete(url=self.cb_host + self._URL_ENTITIES
                                   + entity_id, headers=self.headers)
        return response
