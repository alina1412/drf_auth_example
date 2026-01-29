import asyncio
import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.auth.token_manager import TokenManager
from api.models import Author, Book


@pytest.mark.django_db
def test_list_books_view_success(auth_token):
    url = reverse("book-list")  # URL: /api/books/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }
    client = APIClient()

    author = Author.objects.create(name="Author A")
    Book.objects.create(
        title="Book 1", author=author, publish_date="2020-01-01"
    )
    Book.objects.create(
        title="Book 2", author=author, publish_date="2021-01-01"
    )

    resp = client.get(url, headers=headers)

    assert resp.status_code == 200
    data = resp.json()

    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert isinstance(data, list)
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"Book 1", "Book 2"}


@pytest.mark.django_db
def test_create_book_view_success(auth_token):
    url = reverse("book-list")  # URL: /api/books/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }
    decoded_token_data = TokenManager().decode_token(auth_token)

    client = APIClient()

    author = Author.objects.create(name="Author A")

    book_data = {
        "title": "Test Book Title",
        "author": author.id,
        "publish_date": "2020-01-01",
    }
    response = client.post(
        url,
        data=json.dumps(book_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_create_book_view_failure():
    url = reverse("book-list")  # URL: /api/books/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()

    author = Author.objects.create(name="Author A")

    book_data = {
        "title": "Test Book Title",
        "author": author.id,
        "publish_date": "2020-01-01",
    }
    response = client.post(
        url,
        data=json.dumps(book_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_list_books_view_unauthorized():
    url = reverse("book-list")  # URL: /api/books/
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.get(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_book_view_unauthorized():
    url = reverse("book-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.get(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_update_book_view_unauthorized():
    url = reverse("book-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.put(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_partial_update_book_view_unauthorized():
    url = reverse("book-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.patch(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_delete_book_view_unauthorized():
    url = reverse("book-detail", args=[1])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": "",
    }
    client = APIClient()
    resp = client.delete(url, headers=headers)

    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_book_view(auth_token):
    author = Author.objects.create(name="Author B")
    book = Book.objects.create(
        title="The Book", author=author, publish_date="2022-05-05"
    )

    url = reverse("book-detail", args=[book.pk])  #  /api/books/1/
    client = APIClient()
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    resp = client.get(url, headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == book.pk
    assert data["title"] == "The Book"
    assert data["author"] == author.pk


@pytest.mark.django_db
def test_update_book_view_success(auth_token):
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    author = Author.objects.create(name="Author A")
    book = Book.objects.create(
        title="Original Book", author=author, publish_date="2020-01-01"
    )

    url = reverse("book-detail", args=[book.id])
    update_data = {
        "title": "Updated Book Title",
        "author": author.id,
        "publish_date": "2021-01-01",
    }

    response = client.put(
        url,
        data=json.dumps(update_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_partial_update_book_view_success(auth_token):
    author = Author.objects.create(name="Author A")
    book = Book.objects.create(
        title="Original Book", author=author, publish_date="2020-01-01"
    )

    url = reverse("book-detail", args=[book.id])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    patch_data = {
        "title": "Partially Updated Book",
    }

    response = client.patch(
        url,
        data=json.dumps(patch_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_book_view_success(auth_token):
    author = Author.objects.create(name="Author A")
    book = Book.objects.create(
        title="Book to Delete", author=author, publish_date="2020-01-01"
    )

    url = reverse("book-detail", args=[book.id])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    response = client.delete(url, headers=headers)

    assert response.status_code == 204
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_update_book_view_not_found(auth_token):
    url = reverse("book-detail", args=[999])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    update_data = {"title": "Non-existent Book"}

    response = client.put(
        url,
        data=json.dumps(update_data),
        content_type="application/json",
        headers=headers,
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_book_view_not_found(auth_token):
    url = reverse("book-detail", args=[999])
    headers = {
        "accept": "application/json",
        "Authorization": "bearer xxx",
        "X-Client-Secret": auth_token,
    }

    client = APIClient()
    response = client.delete(url, headers=headers)

    assert response.status_code == 404
