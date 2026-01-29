import json

import pytest
from rest_framework.test import APIClient

from api.auth.token_manager import TokenManager
from api.models import Role, User


@pytest.fixture
def example_basic_role_user() -> dict[str, str]:
    return {
        "username": "joe",
        "password": "123",
        "role": "basic",
    }


@pytest.fixture
def example_admin_role_user() -> dict[str, str]:
    role = Role.objects.get(name="admin")
    user = User.objects.create(
        username="admin",
        password="$2b$12$QfU0BwNI.dJWJ/hEofl/SubOdQYVJ9SLr6qxbZQWiAuNe4yOZiXnS",
        role=role,
    )
    return user


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


@pytest.fixture
def admin_auth_token(example_admin_role_user) -> str:
    """Fixture to get authentication token for ADMIN role user"""
    api_client = APIClient()
    correct_user = example_admin_role_user

    username = correct_user.username
    password = "123"
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
