from django.contrib import admin

from .models import Category, Recipe, Role, User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("name",)


class RecipeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    search_fields = ("title",)


class RoleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    list_filter = ("name",)
    search_fields = ("name",)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "role",
        "is_active",
        "created_at",
        "email",
    )
    list_filter = ("role", "is_active")
    search_fields = ("username", "email")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
