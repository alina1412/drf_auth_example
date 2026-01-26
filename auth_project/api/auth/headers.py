from auth_project.settings import logger


class CredentialsException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


async def validate_bearer_type(request) -> None:
    token_type = request.headers.get("Authorization")
    if not token_type:
        logger.info("no 'Authorization' in a header")

    if not token_type or token_type.split()[0].lower() != "bearer":
        logger.warning("CredentialsException")
        raise CredentialsException(detail="not type 'bearer' in a header")
