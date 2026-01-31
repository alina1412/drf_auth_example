import asyncio
import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.auth.token_manager import TokenManager
from api.models import Category, Recipe


@pytest.mark.django_db
def test_list_recipes_view_success(auth_token):
    url = reverse("recipe-list")  # URL: /api/recipes/
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }
    client = APIClient()

    category = Category.objects.create(name="Category A")
    Recipe.objects.create(
        title="recipe 1", category=category, publish_date="2020-01-01"
    )
    Recipe.objects.create(
        title="recipe 2", category=category, publish_date="2021-01-01"
    )

    resp = client.get(url, headers=headers)

    assert resp.status_code == 200
    data = resp.json()

    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert isinstance(data, list)
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"recipe 1", "recipe 2"}


@pytest.mark.django_db
def test_create_recipe_view_success(auth_token):
    url = reverse("recipe-list")  # URL: /api/recipes/
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }
    decoded_token_data = TokenManager().decode_token(auth_token)

    client = APIClient()

    category = Category.objects.create(name="Category A")

    recipe_data = {
        "title": "Test recipe Title",
        "category": category.id,
        "publish_date": "2020-01-01",
        "description": "lalalalala",
    }
    response = client.post(
        url,
        data=json.dumps(recipe_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_recipe_view_failure():
    url = reverse("recipe-list")  # URL: /api/recipes/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()

    category = Category.objects.create(name="Category A")

    recipe_data = {
        "title": "Test recipe Title",
        "category": category.id,
        "publish_date": "2020-01-01",
    }
    response = client.post(
        url,
        data=json.dumps(recipe_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 401


@pytest.mark.skip(reason="пусть будет доступен")
def test_list_recipes_view_unauthorized():
    url = reverse("recipe-list")  # URL: /api/recipes/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()
    resp = client.get(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_recipe_view_unauthorized():
    url = reverse("recipe-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()
    resp = client.get(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_update_recipe_view_unauthorized():
    url = reverse("recipe-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()
    resp = client.put(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_partial_update_recipe_view_unauthorized():
    url = reverse("recipe-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()
    resp = client.patch(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_delete_recipe_view_unauthorized():
    url = reverse("recipe-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
    }
    client = APIClient()
    resp = client.delete(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_recipe_view(auth_token):
    category = Category.objects.create(name="Category B")
    recipe = Recipe.objects.create(
        title="The recipe", category=category, publish_date="2022-05-05"
    )

    url = reverse("recipe-detail", args=[recipe.pk])  #  /api/recipes/1/
    client = APIClient()
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }
    resp = client.get(url, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == recipe.pk
    assert data["title"] == "The recipe"
    assert data["category"] == category.pk
    assert data["description"] == recipe.description


@pytest.mark.django_db
def test_update_recipe_view_success(auth_token):
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }

    client = APIClient()
    category = Category.objects.create(name="Category A")
    recipe = Recipe.objects.create(
        title="Original recipe", category=category, publish_date="2020-01-01"
    )

    url = reverse("recipe-detail", args=[recipe.id])
    update_data = {
        "title": "Updated recipe Title",
        "category": category.id,
        "publish_date": "2021-01-01",
        "description": "lalalalala",
    }

    response = client.put(
        url,
        data=json.dumps(update_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_partial_update_recipe_view_success(auth_token):
    category = Category.objects.create(name="Category A")
    recipe = Recipe.objects.create(
        title="Original recipe", category=category, publish_date="2020-01-01"
    )

    url = reverse("recipe-detail", args=[recipe.id])
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }

    client = APIClient()
    patch_data = {
        "title": "Partially Updated recipe",
    }

    response = client.patch(
        url,
        data=json.dumps(patch_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_recipe_view_success(auth_token):
    category = Category.objects.create(name="Category A")
    recipe = Recipe.objects.create(
        title="recipe to Delete", category=category, publish_date="2020-01-01"
    )

    url = reverse("recipe-detail", args=[recipe.id])
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }

    client = APIClient()
    response = client.delete(url, headers=headers)

    assert response.status_code == 204
    assert not Recipe.objects.filter(id=recipe.id).exists()


@pytest.mark.django_db
def test_update_recipe_view_not_found(auth_token):
    url = reverse("recipe-detail", args=[999])
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }

    client = APIClient()
    update_data = {"title": "Non-existent recipe"}

    response = client.put(
        url,
        data=json.dumps(update_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_recipe_view_not_found(auth_token):
    url = reverse("recipe-detail", args=[999])
    headers = {
        "accept": "application/json",
        "Authorization": f"bearer {auth_token}",
    }

    client = APIClient()
    response = client.delete(url, headers=headers)

    assert response.status_code == 404
