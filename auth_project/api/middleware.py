from urllib import request

from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from api.auth.utils import get_user_token_data
from auth_project.settings import logger

AUTH_REQUIRED_PATHS = ["/api/books-author/", "/api/books/"]


class AsyncMiddleware0:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def do_before(self, request):
        for optional_path in AUTH_REQUIRED_PATHS:
            if request.path.startswith(optional_path):
                token = await get_user_token_data(request)
                return token
        return None

    async def __call__(self, request):
        logger.debug("AsyncMiddleware0 before request")
        token = await self.do_before(request)
        response = await self.get_response(request)
        # Some logic ...

        return response


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
