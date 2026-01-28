import asyncio
import json
from urllib import request

from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.decorators import (
    require_admin_role,
    require_basic_role,
    require_manager_role,
)
from api.auth.schemas import UserDataDto, UserRole
from api.auth.serializers import LoginSerializer
from api.auth.token_manager import TokenManager
from api.auth.utils import UserAccessDb, UserAuthorization
from auth_project.settings import logger

from .models import Book, Role, User
from .serializers import BookAuthorSerializer, BookSerializer


@require_basic_role
class BookViewSet(viewsets.ModelViewSet):
    """Shows books"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")

    # GET
    @require_basic_role
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    @require_manager_role
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class BookAuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for books with full author details
    """

    serializer_class = BookAuthorSerializer
    queryset = Book.objects.all().select_related("author").order_by("id")

    # GET
    @require_basic_role
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    @require_manager_role
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


@require_basic_role
class TokenGenView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: "Token response"}
    )
    def post(self, request):
        token = TokenManager().generate_token(request)
        return Response(
            {"token": token, "token_type": "bearer"}, status=status.HTTP_200_OK
        )


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer, responses={201: "User registered"}
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            UserAccessDb().save_user(username, password)
        except Exception as e:
            logger.error(f"User registration failed: {e}")
            return Response(
                {"error": "User registration failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED,
        )
