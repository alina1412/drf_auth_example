import json

import pytest
from rest_framework.test import APIClient

from api.auth.token_manager import TokenManager


@pytest.fixture
def example_basic_role_user() -> dict[str, str]:
    return {
        "username": "joe",
        "password": "123",
        "role": "basic",
    }


@pytest.fixture
def auth_token(example_basic_role_user) -> str:
    """Fixture to get authentication token for BASIC role user"""
    api_client = APIClient()
    correct_user = example_basic_role_user

    username = correct_user["username"]
    password = correct_user["password"]
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
    decoded_token_data = TokenManager().decode_token(data["token"])
    return data["token"]
