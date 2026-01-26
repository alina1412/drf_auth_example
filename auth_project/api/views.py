from django.shortcuts import render
from rest_framework import viewsets

from .models import Book
from .serializers import BookAuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Shows books"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookAuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for books with full author details
    """

    serializer_class = BookAuthorSerializer
    queryset = Book.objects.all().select_related("author").order_by("id")
