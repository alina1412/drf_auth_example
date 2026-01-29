import json

from auth_project.settings import logger

from api.auth.db import UserAccessDb

from .exceptions import (
    CredentialsException,
    CredentialsException401,
    CredentialsException422,
    CredentialsExceptionResponse,
)
from .schemas import UserDataDto, UserRole
from .token_manager import TokenManager
from .utils import EncodingPassword


class UserAuthorization:
    @staticmethod
    def process_access(role: UserRole, require_role: UserRole) -> bool:
        if not UserRole.has_permission(role, require_role):
            return False

        return True

    @staticmethod
    def verify_user(user: UserDataDto, password: str) -> bool:
        if not user:
            return False
        if not user.is_active or not EncodingPassword.verify_password(
            user.password, password
        ):
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

    def auth_user(self, request) -> None:
        """Если пользователь не верифицирован,
        ошибка 401"""
        try:
            body = json.loads(request.body)
            assert "username" in body and "password" in body
        except (json.JSONDecodeError, AssertionError):
            logger.info("Invalid JSON in request body")
            raise CredentialsException422()

        guest_user = self.unverified_user(body)
        user = UserAccessDb().get_user({"username": guest_user.username})

        if not self.verify_user(user, guest_user.password):
            logger.info("User is not verified")
            raise CredentialsException401()

        request.user_data = user

    def auth_user_by_token(self, request, token: str) -> None:
        try:
            self.validate_bearer_type(request)
            token_info = TokenManager().check_token(token, request)
        except CredentialsException as exc:
            logger.debug(f"Token validation error: {exc.detail}")
            raise CredentialsException(
                detail="Token validation error"
            ) from exc
        request.user_data.username = token_info.claims.username
        request.user_data.role = UserRole(token_info.claims.role)

    @staticmethod
    def validate_bearer_type(request) -> None:
        token_type = request.headers.get("Authorization")
        logger.debug(f"auth_header1 token_type: {token_type}")
        if not token_type:
            logger.info("no 'Authorization' in a header")

        if not token_type or token_type.split()[0].lower() != "bearer":
            logger.warning("CredentialsException")
            raise CredentialsException(detail="not type 'bearer' in a header")
