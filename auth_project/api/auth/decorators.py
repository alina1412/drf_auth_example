from auth_project.settings import logger

from api.auth.exceptions import (
    CredentialsException,
    CredentialsException401,
    CredentialsException403,
    CredentialsException422,
    CredentialsExceptionResponse,
)
from api.auth.schemas import UserRole
from api.auth.user_auth import UserAuthorization


def auth_by_creds():
    def decorator(func):
        def wrapped(view_, request, *args, **kwargs):
            logger.debug("Decorator auth_by_creds applied")

            try:
                UserAuthorization().auth_user(request)
            except CredentialsException401:
                return CredentialsExceptionResponse().response_401()
            except CredentialsException422:
                return CredentialsExceptionResponse().response_422()

            return func(view_, request, *args, **kwargs)

        return wrapped

    return decorator


def require_auth_role(reqired_role):
    def decorator(func):
        def wrapped(view_, request, *args, **kwargs):
            logger.debug(f"Decorator {reqired_role} applied")

            auth_class = UserAuthorization()

            if not auth_class.validate_bearer_type(request):
                return CredentialsExceptionResponse().response_401()

            token = auth_class.token
            logger.debug(f"token from header: {token}")
            verified_token = False

            if token:
                try:
                    auth_class.auth_user_by_token(request)
                    verified_token = True
                except CredentialsException as exc:
                    logger.debug(f"User is not verified {exc}")

            if not verified_token:
                return CredentialsExceptionResponse().response_401()

            if not auth_class.process_access(
                request.user_data.role, reqired_role
            ):
                return CredentialsExceptionResponse().response_403()

            return func(view_, request, *args, **kwargs)

        return wrapped

    return decorator
