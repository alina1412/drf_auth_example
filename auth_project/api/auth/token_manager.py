import datetime

import pytz
from auth_project.settings import logger
from jose import JWTError, jwt

from api.auth.db import UserAccessDb
from api.auth.exceptions import CredentialsException
from api.auth.schemas import TokenCheckedDataDto, TokenDataDto, UserDataDto

SECRET = "your_secret_key_here"


class TokenManager:
    ALGORITHM = "HS256"

    def get_data_for_token(
        self, user_data: UserDataDto, timedelta_min=30
    ) -> dict[str, str]:
        expire = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(
            minutes=timedelta_min
        )
        expire = expire.isoformat()
        data_to_encode = {
            "username": user_data.username,
            "expire": expire,
            "role": user_data.role.value,
        }
        return data_to_encode

    def generate_token(self, request, algorithm: str | None = None) -> str:
        """Make token by jwt.encode"""
        algorithm = self.ALGORITHM if not algorithm else algorithm
        data_to_encode = self.get_data_for_token(request.user_data)
        token = jwt.encode(
            claims=data_to_encode, key=SECRET, algorithm=algorithm
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
            data = jwt.decode(token, SECRET, algorithms=algorithm)
        except JWTError as exc:
            raise CredentialsException(detail="Incorrect token") from exc

        return TokenDataDto(**data)

    def validate_token(self, user: UserDataDto, expired_time: str) -> None:
        if (
            not user
            or not user.is_active
            or expired_time is None
            or datetime.datetime.fromisoformat(expired_time)
            < datetime.datetime.now(tz=pytz.utc)
        ):
            raise CredentialsException(detail="expired token")

    def check_token(self, token: str, request) -> TokenCheckedDataDto:
        decoded_token_data = self.decode_token(token)
        user = UserAccessDb().get_user(
            {"username": decoded_token_data.username}
        )
        expired_time = decoded_token_data.expire
        self.validate_token(user, expired_time)
        request.user_data = user
        return TokenCheckedDataDto(
            **{
                "token": "valid",
                "claims": decoded_token_data,
                "token_type": "bearer",
            }
        )
