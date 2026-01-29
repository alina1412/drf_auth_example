from django.http import JsonResponse


class CredentialsException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class CredentialsException401(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class CredentialsException403(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class CredentialsException422(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class CredentialsExceptionResponse:
    def response_401(self):
        return JsonResponse({"error": "Unauthorized"}, status=401)

    def response_403(self):
        return JsonResponse({"error": "Forbidden"}, status=403)

    def response_422(self):
        return JsonResponse({"error": "Bad Request"}, status=422)
