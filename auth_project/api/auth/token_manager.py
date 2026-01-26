import datetime

import pytz
from jose import JWTError, jwt


from auth_project.api.auth.fake_db import get_user
from auth_project.api.auth.headers import CredentialsException
from auth_project.api.auth.schemas import TokenCheckedDataDto, TokenDataDto

SECRET = "your_secret_key_here"


class TokenManager:
    ALGORITHM = "HS256"

    def get_data_for_token(
        self, username: str, timedelta_min=30
    ) -> dict[str, str]:
        expire = datetime.datetime.now(tz=pytz.utc) + datetime.timedelta(
            minutes=timedelta_min
        )
        expire = expire.isoformat()
        data_to_encode = {"username": username, "expire": expire}
        return data_to_encode

    def generate_token(
        self, username: str, algorithm: str | None = None
    ) -> str:
        """Make token by jwt.encode"""
        algorithm = self.ALGORITHM if not algorithm else algorithm
        data_to_encode = self.get_data_for_token(username)
        token = jwt.encode(
            claims=data_to_encode, key=SECRET, algorithm=algorithm
        )
        return token

    def decode_token(
        self, token: str, algorithm: str | None = None
    ) -> TokenDataDto:
        algorithm = self.ALGORITHM if not algorithm else algorithm
        try:
            data = jwt.decode(token, SECRET, algorithms=algorithm)
        except JWTError as exc:
            raise CredentialsException(detail="Incorrect token") from exc
        return TokenDataDto(**data)

    def validate_token(self, user: dict, expired_time: str) -> None:
        if (
            not user
            or expired_time is None
            or datetime.datetime.fromisoformat(expired_time)
            < datetime.datetime.now(tz=pytz.utc)
        ):
            raise CredentialsException(detail="expired token")

    def check_token(self, token: str) -> TokenCheckedDataDto:
        decoded_token_data = self.decode_token(token)
        user = get_user(decoded_token_data.username)
        expired_time = decoded_token_data.expire
        self.validate_token(user, expired_time)
        return TokenCheckedDataDto(
            **{
                "token": "valid",
                "claims": decoded_token_data,
                "token_type": "bearer",
            }
        )
