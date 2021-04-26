import requests

CONTENT_TYPE_HEADER = {"Content-Type": "application/x-www-form-urlencoded"}


def get_token(auth_server_host, client_id, client_secret, grant_type):
    try:
        response = requests.post(
            url=auth_server_host,
            headers=CONTENT_TYPE_HEADER,
            params={"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type}
        )
        response.raise_for_status()
        json_response = response.json()
        return json_response["access_token"]
    except Exception as err:
        print(f'Error encountered while requesting token from authentication server: {err}')
        return None
