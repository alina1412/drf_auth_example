from urllib import request
from asgiref.sync import iscoroutinefunction, markcoroutinefunction

from drf_example.settings import logger


class AsyncMiddleware0:
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def __call__(self, request):
        logger.debug("AsyncMiddleware0 before request")
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
