import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from api.models import Author, Book


@pytest.mark.django_db
def test_list_books_view():
    author = Author.objects.create(name="Author A")
    Book.objects.create(
        title="Book 1", author=author, publish_date="2020-01-01"
    )
    Book.objects.create(
        title="Book 2", author=author, publish_date="2021-01-01"
    )

    client = APIClient()
    url = reverse("book-list")  # URL: /api/books/
    resp = client.get(url)

    assert resp.status_code == 200
    data = resp.json()

    if isinstance(data, dict) and "results" in data:
        data = data["results"]

    assert isinstance(data, list)
    assert len(data) == 2
    titles = {item["title"] for item in data}
    assert titles == {"Book 1", "Book 2"}


@pytest.mark.django_db
def test_get_book_view():
    author = Author.objects.create(name="Author B")
    book = Book.objects.create(
        title="The Book", author=author, publish_date="2022-05-05"
    )

    client = APIClient()
    url = reverse("book-detail", args=[book.pk])  #  /api/books/1/
    resp = client.get(url)

    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == book.pk
    assert data["title"] == "The Book"
    assert data["author"] == author.pk
