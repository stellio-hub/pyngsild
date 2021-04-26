import pytest
from pyngsild.ctxbroker import ContextBroker
from pyngsild.entity import Entity

CONTEXT_BROKER_URL = "http://localhost:5000/"
QUERY_ENTITIES_EXPECTATION = [
    Entity('urn:ngsi-ld:Vehicle:01231', 'Vehicle').to_ngsild(),
    Entity('urn:ngsi-ld:Vehicle:01232', 'Vehicle').to_ngsild()
]


class TestContextBroker:

    def set_up(self):
        self.context_broker = ContextBroker(CONTEXT_BROKER_URL)

    @pytest.mark.server(
        url='/ngsi-ld/v1/entities/',
        method='GET',
        headers={'Authorization': 'Bearer token'},
        response=QUERY_ENTITIES_EXPECTATION
    )
    def test_query_entities(self):
        self.set_up()
        response = self.context_broker.query_entities(
            {'Authorization': 'Bearer token'},
            {'type': "Vehicle", 'idPattern': '^urn:ngsi-ld:Vehicle:.*'}
        )
        assert response.status_code == 200
        assert response.json() == QUERY_ENTITIES_EXPECTATION
