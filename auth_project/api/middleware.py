from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from api.auth.exceptions import (
    CredentialsException,
    CredentialsExceptionResponse,
)
from api.auth.schemas import UserDataDto, UserRole
from api.auth.utils import UserAuthorization
from auth_project.settings import logger

from .views import RegistrationView, TokenGenView

AUTH_REQUIRED_PATHS = ["/api/books-author/", "/api/books/", "/api/token/gen"]


class AsyncMiddleware0:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def do_before(self, request):
        guest_data = UserDataDto(username="", password="", role=UserRole.GUEST)
        request.user_data = guest_data

    async def __call__(self, request):
        logger.debug("AsyncMiddleware0 before request")
        await self.do_before(request)
        response = await self.get_response(request)
        # Some logic after...

        return response

    async def process_view(self, request, view_func, view_args, view_kwargs):
        view_class = getattr(view_func, "cls", None)
        token = request.headers.get("X-Client-Secret")
        logger.debug(f"token from header: {token}")
        verified_token = False

        # if view_class == RegistrationView and request.method == "POST":
        #     return None
        if view_class == TokenGenView:
            return UserAuthorization.auth_user(request)

        if token:
            try:
                await UserAuthorization.auth_user_by_token(request, token)
                verified_token = True
            except CredentialsException as exc:
                logger.debug("User is not verified")

        if hasattr(view_class, "require_role"):
            if not verified_token:
                return CredentialsExceptionResponse().response_401()

            if not UserAuthorization.process_access(
                request.user_data.role, view_class.require_role
            ):
                return CredentialsExceptionResponse().response_403()


class AsyncMiddleware1:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        logger.debug("AsyncMiddleware1 before request")
        response = await self.get_response(request)
        # Some logic ...

        return response
