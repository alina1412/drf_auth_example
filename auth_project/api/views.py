import asyncio
import json

from auth_project.settings import logger
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth.db import RoleAccessDb, UserAccessDb
from api.auth.decorators import (
    auth_by_creds,
    require_auth_role,
)
from api.auth.exceptions import (
    CredentialsException403,
    CredentialsExceptionResponse,
)
from api.auth.schemas import UserDataDto, UserRole
from api.auth.serializers import LoginSerializer, UserRoleEditSerializer
from api.auth.token_manager import TokenManager

from .models import Book, User
from .serializers import BookAuthorSerializer, BookSerializer, UserSerializer


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
    # Разрешить просмотр списка книг без авторизации
    def list(self, request, *args, **kwargs):
        """Shows list of books"""
        return super().list(request, *args, **kwargs)

    # POST
    @require_auth_role(UserRole.BASIC)
    def create(self, request, *args, **kwargs):
        """Creates a book"""
        return super().create(request, *args, **kwargs)

    @require_auth_role(UserRole.BASIC)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    # PATCH partial update
    @require_auth_role(UserRole.BASIC)
    def partial_update(self, request, *args, **kwargs):
        """Updates a book's data partially"""
        return super().partial_update(request, *args, **kwargs)

    # DELETE book
    @require_auth_role(UserRole.BASIC)
    def destroy(self, request, *args, **kwargs):
        """Deletes a book"""
        return super().destroy(request, *args, **kwargs)


class BookAuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for books with full author details
    """

    serializer_class = BookAuthorSerializer
    queryset = Book.objects.all().select_related("author").order_by("id")

    @require_auth_role(UserRole.GUEST)
    def list(self, request, *args, **kwargs):
        """Shows list of books with their authors"""
        return super().list(request, *args, **kwargs)

    # POST
    @require_auth_role(UserRole.BASIC)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class TokenGenView(APIView):
    """
    Generates token with a limited access time
    """

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
        """Registers a new user (profile)"""
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        # This is MVP: it's not checked if email is correct
        # It's not connected to django User database, could be edited later

        try:
            UserAccessDb().save_user(username, password, email)
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


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("id")
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
    @require_auth_role(UserRole.ADMIN)
    def list(self, request, *args, **kwargs):
        """Shows list of users"""
        return super().list(request, *args, **kwargs)

    # POST
    @require_auth_role(UserRole.ADMIN)
    def create(self, request, *args, **kwargs):
        """Creates a user"""
        return super().create(request, *args, **kwargs)

    @require_auth_role(UserRole.BASIC)
    def update(self, request, *args, **kwargs):
        """Updates user profile by himself or by admin, by id"""
        if request.user_data.role != UserRole.ADMIN:
            try:
                user = self.get_own_profile_or_403(request)
                if "role" in request.data:
                    del request.data["role"]

            except CredentialsException403:
                return Response(
                    {"error": "Incorrect request."},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return super().update(request, *args, **kwargs)

    # PATCH partial update
    @require_auth_role(UserRole.BASIC)
    def partial_update(self, request, *args, **kwargs):
        """Updates user profile partiially by himself or by admin, by id"""
        if request.user_data.role != UserRole.ADMIN:
            try:
                user = self.get_own_profile_or_403(request)

                if "role" in request.data:
                    del request.data["role"]

            except CredentialsException403:
                return Response(
                    {"error": "Incorrect request."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().partial_update(request, *args, **kwargs)

    def get_own_profile_or_403(self, request) -> User:
        pk = self.kwargs["pk"]
        user = get_object_or_404(self.get_queryset(), pk=pk)

        if not request.user_data.username == user.username:
            raise CredentialsException403()

        return user

    # DELETE -> set is_active=False
    @require_auth_role(UserRole.BASIC)
    def destroy(self, request, *args, **kwargs):
        """Deactivates user profile by himself or by admin, by id"""
        try:
            user = self.get_own_profile_or_403(request)
        except CredentialsException403:
            return Response(
                {"error": "Incorrect request."},
                status=status.HTTP_403_FORBIDDEN,
            )

        user.is_active = False
        user.save()
        request.user_data.role = UserRole.GUEST
        request.user_data.username = "guest"
        request.user_data.is_active = False
        return Response(status=status.HTTP_200_OK)


class UsersRoleEditView(APIView):
    @swagger_auto_schema(
        request_body=UserRoleEditSerializer,
        responses={200: "success", 404: "user not found", 422: "Bad Request"},
    )
    @require_auth_role(UserRole.ADMIN)
    def post(self, request):
        """The functionality of editing role of users by id for admins"""
        user_id = request.data.get("id")
        role_id = request.data.get("role_id")

        if not (isinstance(user_id, int) and isinstance(role_id, int)):
            return CredentialsExceptionResponse().response_422()

        try:
            user = User.objects.filter(id=user_id).first()
            if not user:
                return Response(
                    {"error": "user not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            role = RoleAccessDb().get_role({"id": role_id})
            user.role = role
            user.save()
        except Exception as e:
            logger.error(f"User edit failed: {e}")
            return Response(
                {"error": "User edit failed", "details": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "success"},
            status=status.HTTP_200_OK,
        )
