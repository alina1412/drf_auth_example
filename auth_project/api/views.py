from urllib import request

from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema

from api.auth.fake_db import get_user
from api.auth.headers import CredentialsException
from api.auth.serializers import LoginSerializer
from api.auth.token_manager import TokenManager
from api.auth.utils import verify_user

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


class TokenGenView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: "Token response"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = get_user(username)
        if not verify_user(user, password):
            raise CredentialsException(
                detail="Incorrect username or password",
            )
        token = TokenManager().generate_token(username)
        return Response(
            {"token": token, "token_type": "bearer"}, status=status.HTTP_200_OK
        )
