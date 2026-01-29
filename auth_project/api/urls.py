from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    BookAuthorViewSet,
    BookViewSet,
    RegistrationView,
    TokenGenView,
    UsersRoleEditView,
    UserViewSet,
)

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register(r"books-author", BookAuthorViewSet, basename="bookauthor")
router.register("profile", UserViewSet, basename="profile")


schema_view = get_schema_view(
    openapi.Info(
        title="Custom API",
        default_version="v1",
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = router.urls + [
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("token/gen", TokenGenView.as_view(), name="token-gen"),
    path("register", RegistrationView.as_view(), name="register"),
    path("edit-role", UsersRoleEditView.as_view(), name="edit-role"),
]
