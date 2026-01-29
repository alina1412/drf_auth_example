import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.auth.schemas import UserRole
from api.auth.token_manager import TokenManager
from api.models import Role, User


@pytest.mark.django_db
def test_registration_success():
    client = APIClient()
    url = reverse("register")

    user_data = {"username": "testuser", "password": "testpass123"}

    response = client.post(
        url, data=json.dumps(user_data), content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_registration_missing_username():
    client = APIClient()
    url = reverse("register")

    user_data = {"password": "testpass123"}

    response = client.post(
        url, data=json.dumps(user_data), content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_missing_password():
    client = APIClient()
    url = reverse("register")

    user_data = {"username": "testuser"}

    response = client.post(
        url, data=json.dumps(user_data), content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_registration_duplicate_username():
    client = APIClient()
    url = reverse("register")

    user_data = {"username": "testuser", "password": "testpass123"}

    response1 = client.post(
        url, data=json.dumps(user_data), content_type="application/json"
    )

    response2 = client.post(
        url, data=json.dumps(user_data), content_type="application/json"
    )

    assert response1.status_code == 201
    assert response2.status_code == 400


@pytest.mark.django_db
def test_registration_empty_data():
    client = APIClient()
    url = reverse("register")

    response = client.post(
        url, data=json.dumps({}), content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_get_user_view_unauthorized():
    url = reverse("profile-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.get(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_delete_own_profile_view_success(auth_token, example_basic_role_user):
    profile = User.objects.get(username=example_basic_role_user["username"])

    url = reverse("profile-detail", args=[profile.id])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    response = client.delete(url, headers=headers)

    assert response.status_code == 200
    result_user = User.objects.filter(id=profile.id).first()
    assert result_user.is_active == False

    url = reverse("profile-detail", args=[profile.id])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    response = client.get(url, headers=headers)
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_other_user_view_forbidden(auth_token):
    role = Role.objects.create(name=UserRole.BASIC)
    new_user = User.objects.create(
        username="to Delete", password="author", role=role
    )
    url = reverse("profile-detail", args=[new_user.id])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }
    client = APIClient()
    resp = client.delete(url, headers=headers)

    assert resp.status_code == 403
