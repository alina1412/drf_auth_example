from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "name"]


class BookAuthorSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = "__all__"

    def create(self, validated_data):
        author_data = validated_data.pop("author")

        author, created = Author.objects.get_or_create(**author_data)
        book = Book.objects.create(author=author, **validated_data)

        return book
