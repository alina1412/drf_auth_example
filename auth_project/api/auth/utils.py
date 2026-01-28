import json

import bcrypt

from api.auth.fake_db import fake_db, get_user
from api.models import Role, User
from auth_project.settings import logger

from .exceptions import CredentialsException, CredentialsExceptionResponse
from .schemas import TokenDataDto, UserDataDto, UserRole
from .token_manager import TokenManager


class UserAuthorization:
    @staticmethod
    def process_access(role: UserRole, require_role: UserRole) -> bool:
        if not UserRole.has_permission(role, require_role):
            return False

        return True

    @staticmethod
    def verify_password(password_in_db: str, raw_password: str) -> bool:
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), password_in_db.encode("utf-8")
        )

    @staticmethod
    def set_password(raw_password: str) -> str:
        password_hash = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        )
        return password_hash

    @staticmethod
    def verify_user(user: UserDataDto, password: str) -> bool:
        if not user:
            return False
        if not UserAuthorization.verify_password(user.password, password):
            return False
        return True

    @staticmethod
    def unverified_user(body) -> UserDataDto:
        user_data = UserDataDto(
            username=body.get("username", ""),
            password=body.get("password", ""),
            role=UserRole.GUEST,
        )
        return user_data

    @staticmethod
    def auth_user(request) -> UserDataDto | None:
        """Если пользователь не верифицирован,
        ошибка 401"""
        try:
            body = json.loads(request.body)
            assert "username" in body and "password" in body
        except (json.JSONDecodeError, AssertionError):
            logger.info("Invalid JSON in request body")
            return CredentialsExceptionResponse().response_422()

        guest_user = UserAuthorization.unverified_user(body)
        user = get_user(guest_user.username)

        if not UserAuthorization.verify_user(user, guest_user.password):
            logger.info("User is not verified")
            return CredentialsExceptionResponse().response_401()

        request.user_data = user

    @staticmethod
    async def auth_user_by_token(request, token: str) -> TokenDataDto:
        try:
            UserAuthorization.validate_bearer_type(request)
            token_info = TokenManager().check_token(token, request)
        except CredentialsException as exc:
            logger.debug(f"Token validation error: {exc.detail}")
            raise CredentialsException(
                detail="Token validation error"
            ) from exc
        request.user_data.username = token_info.claims.username
        request.user_data.role = UserRole(token_info.claims.role)

    @staticmethod
    async def validate_bearer_type(request) -> None:
        token_type = request.headers.get("Authorization")
        logger.debug(f"auth_header1 token_type: {token_type}")
        if not token_type:
            logger.info("no 'Authorization' in a header")

        if not token_type or token_type.split()[0].lower() != "bearer":
            logger.warning("CredentialsException")
            raise CredentialsException(detail="not type 'bearer' in a header")


class UserAccessDb:
    def save_user(self, username: str, password: str) -> None:
        role = Role.objects.filter(name="basic").first()
        hashed_password = UserAuthorization.set_password(password)
        guest_user = UserDataDto(
            username=username,
            password=hashed_password,
            role=UserRole.BASIC,
        )
        user = User(
            username=guest_user.username,
            password=guest_user.password,
            role=role,
        )
        user.save()

        fake_db[username] = {
            "username": guest_user.username,
            "password": guest_user.password,
            "role": guest_user.role.value,
        }
