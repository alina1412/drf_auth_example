import asyncio
import json

from auth_project.settings import logger
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.decorators import (
    auth_by_creds,
    require_auth_role,
)
from api.auth.schemas import UserDataDto, UserRole
from api.auth.serializers import LoginSerializer
from api.auth.token_manager import TokenManager
from api.auth.utils import UserAccessDb, UserAuthorization

from .models import Book, Role, User
from .serializers import BookAuthorSerializer, BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """Shows books"""

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")
    lookup_field = "pk"

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        pk = self.kwargs["pk"]
        return get_object_or_404(self.get_queryset(), pk=pk)

    @require_auth_role(UserRole.BASIC)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # GET
    @require_auth_role(UserRole.BASIC)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    @require_auth_role(UserRole.BASIC)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @require_auth_role(UserRole.BASIC)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # PATCH partial update
    @require_auth_role(UserRole.BASIC)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    # DELETE book
    @require_auth_role(UserRole.BASIC)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookAuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for books with full author details
    """

    serializer_class = BookAuthorSerializer
    queryset = Book.objects.all().select_related("author").order_by("id")

    @require_auth_role(UserRole.GUEST)
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # POST
    @require_auth_role(UserRole.BASIC)
    async def create(self, request, *args, **kwargs):
        return await super().create(request, *args, **kwargs)


class TokenGenView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer, responses={200: "Token response"}
    )
    @auth_by_creds()
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
