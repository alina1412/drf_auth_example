from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from auth_project.settings import logger

from api.auth.exceptions import (
    CredentialsException,
    CredentialsExceptionResponse,
)
from api.auth.schemas import UserDataDto, UserRole
from api.auth.user_auth import UserAuthorization

from .views import RegistrationView, TokenGenView

AUTH_REQUIRED_PATHS = ["/api/books-author/", "/api/books/", "/api/token/gen"]


class AsyncMiddleware0:
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def do_before(self, request):
        guest_data = UserDataDto(username="", password="", role=UserRole.GUEST)
        request.user_data = guest_data

    def __call__(self, request):
        logger.debug("AsyncMiddleware0 before request")
        self.do_before(request)
        response = self.get_response(request)
        # Some logic after...

        return response


class AsyncMiddleware1:
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("AsyncMiddleware1 before request")
        response = self.get_response(request)
        # Some logic ...

        return response
