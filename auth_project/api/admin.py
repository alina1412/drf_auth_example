from django.contrib import admin

from .models import Author, Book


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")
    search_fields = ("name",)


class BookAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    search_fields = ("title",)


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
