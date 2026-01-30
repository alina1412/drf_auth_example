from django.urls import path
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


urlpatterns = router.urls + [
    path("token/gen", TokenGenView.as_view(), name="token-gen"),
    path("register", RegistrationView.as_view(), name="register"),
    path(
        "profile/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="profile-list",
    ),
    path(
        "profile/<int:pk>/",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="profile-detail",
    ),
    path("edit-role", UsersRoleEditView.as_view(), name="edit-role"),
    path(
        "books/",
        BookViewSet.as_view({"get": "list", "post": "create"}),
        name="book-list",
    ),
    path(
        "books/<int:pk>/",
        BookViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="book-detail",
    ),
    path(
        "books-author/",
        BookAuthorViewSet.as_view({"get": "list", "post": "create"}),
        name="bookauthor-list",
    ),
    path(
        "books-author/<int:pk>/",
        BookAuthorViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="bookauthor-detail",
    ),
]
