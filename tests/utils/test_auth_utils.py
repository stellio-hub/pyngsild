import pytest
from pyngsild.utils.auth_utils import get_token

AUTH_SERVER_URL = "http://localhost:5000/auth"
CLIENT_ID = "client_id"
CLIENT_SECRET = "client_secret"
GRANT_TYPE = "client_credentials"


class TestAuthUtils:

    @pytest.mark.server(
        url='/auth',
        method='POST',
        response={"access_token": "token"}
    )
    def test_get_token(self):
        token = get_token(AUTH_SERVER_URL, CLIENT_ID, CLIENT_SECRET, GRANT_TYPE)
        assert token == "token"

    @pytest.mark.server(
        url='/auth/fail',
        method='POST',
        response={"error": "Error encountered while requesting token from authentication server"}
    )
    def test_get_token_fail(self):
        token = get_token(AUTH_SERVER_URL + "/fail", CLIENT_ID, CLIENT_SECRET, GRANT_TYPE)
        assert token is None
