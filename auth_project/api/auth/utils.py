from passlib.context import CryptContext

from auth_project.settings import logger

# from service.exceptions import CredentialsException
from .headers import validate_bearer_type
from .schemas import TokenDataDto
from .token_manager import TokenManager

hasher = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


class CredentialsException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


def verify_password(user: dict, password: str) -> bool:
    password_in_db = user.get("password")
    return hasher.verify(password, password_in_db)


def verify_user(user: dict, password: str) -> bool:
    if not user:
        return False
    if not verify_password(user, password):
        return False
    return True


async def get_user_token_data(
    request,  # =(validate_bearer_type)
) -> TokenDataDto:
    token = ""
    auth_header1 = request.headers.get("Authorization")
    logger.debug(f"auth_header1: {auth_header1}")

    token = request.headers.get("X-Client-Secret")
    logger.debug(f"found client_secret in header with key: {token}")

    logger.debug(f"token from header: {token}")
    if token is None:
        logger.info("no 'client_secret' in a header")
        raise CredentialsException(detail="no 'client_secret' in a header")

    token_info = TokenManager().check_token(token)
    return token_info.claims
