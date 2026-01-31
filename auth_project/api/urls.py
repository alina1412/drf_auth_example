from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    RecipeCategoryViewSet,
    RecipeViewSet,
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
        "recipes/",
        RecipeViewSet.as_view({"get": "list", "post": "create"}),
        name="recipe-list",
    ),
    path(
        "recipes/<int:pk>/",
        RecipeViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="recipe-detail",
    ),
    path(
        "recipes-category/",
        RecipeCategoryViewSet.as_view({"get": "list", "post": "create"}),
        name="recipe-category-list",
    ),
    path(
        "recipes-category/<int:pk>/",
        RecipeCategoryViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="recipe-category-detail",
    ),
]
