from auth_project.settings import logger

from api.auth.schemas import UserDataDto, UserRole


class GuestUserMiddleware:
    sync_capable = True

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.debug("GuestUserMiddleware before request")

        request.user_data = UserDataDto(
            username="", password="", role=UserRole.GUEST
        )
        response = self.get_response(request)
        # Some logic after...

        return response
