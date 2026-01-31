import datetime
import os

import pytz
from auth_project.settings import logger
from jose import JWTError, jwt

from api.auth.db import UserAccessDb
from api.auth.exceptions import CredentialsException
from api.auth.schemas import TokenCheckedDataDto, TokenDataDto, UserDataDto
from api.models import Token

TOKENSECRET = os.environ.get("TOKENSECRET")


class TokenManager:
    ALGORITHM = "HS256"

    def get_data_for_token(
        self, user_data: UserDataDto, version: int, timedelta_min=30
    ) -> dict[str, str]:
        expire = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(
            minutes=timedelta_min
        )
        expire = expire.isoformat()
        data_to_encode = {
            "id": user_data.id,
            "username": user_data.username,
            "expire": expire,
            "role": user_data.role.value,
            "version": version,
        }
        return data_to_encode

    def mark_token_version(self, request):
        from django.db.models import F

        token_obj, created = Token.objects.get_or_create(
            user_id=request.user_data.id, defaults={"version": 1}
        )
        if not created:
            token_obj.version = F("version") + 1
            token_obj.save()

        return token_obj.version

    def generate_token(
        self, request, version, algorithm: str | None = None
    ) -> str:
        """Make token by jwt.encode"""
        algorithm = self.ALGORITHM if not algorithm else algorithm
        data_to_encode = self.get_data_for_token(request.user_data, version)
        token = jwt.encode(
            claims=data_to_encode, key=TOKENSECRET, algorithm=algorithm
        )
        return token

    def decode_token(
        self, token: str, algorithm: str | None = None
    ) -> TokenDataDto:
        if not token:
            logger.debug("No token provided")
            raise CredentialsException(detail="No token provided")

        algorithm = self.ALGORITHM if not algorithm else algorithm

        try:
            data = jwt.decode(token, TOKENSECRET, algorithms=algorithm)
        except JWTError as exc:
            raise CredentialsException(detail="Incorrect token") from exc

        return TokenDataDto(**data)

    def validate_token(self, decoded_token_data: TokenDataDto) -> None:
        if (
            decoded_token_data.expire is None
            or datetime.datetime.fromisoformat(decoded_token_data.expire)
            < datetime.datetime.now(tz=pytz.utc)
        ):
            raise CredentialsException(detail="expired token")

        token_obj = Token.objects.filter(user_id=decoded_token_data.id).first()

        if (
            not token_obj
            or not token_obj.version == decoded_token_data.version
        ):
            raise CredentialsException(detail="Incorrect token")

    def check_token(self, token: str, request) -> TokenCheckedDataDto:
        decoded_token_data = self.decode_token(token)
        # user = UserAccessDb().get_user(
        #     {"username": decoded_token_data.username}
        # )
        expired_time = decoded_token_data.expire
        self.validate_token(decoded_token_data)
        # request.user_data = user
        return TokenCheckedDataDto(
            **{
                "token": "valid",
                "claims": decoded_token_data,
                "token_type": "bearer",
            }
        )
