import json

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def auth_token():  # api_client
    """Fixture to get authentication token"""
    api_client = APIClient()
    CORRECT_USER = {"username": "joe", "password": "123"}

    username = CORRECT_USER["username"]
    password = CORRECT_USER["password"]
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }

    response = api_client.post(
        "/api/token/gen",
        data={"username": username, "password": password},
        format="json",
        **headers,
    )

    assert response.status_code == 200
    data = json.loads(response.content)
    return data["token"]
