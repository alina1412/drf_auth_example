from django.contrib import admin

from .models import Author, Book, Role, User


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("name",)


class BookAdmin(admin.ModelAdmin):
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


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
