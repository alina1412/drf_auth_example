from rest_framework import serializers

from .models import Category, Recipe, User


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class RecipeCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Recipe
        fields = "__all__"

    def create(self, validated_data):
        new_data = validated_data.pop("category")

        new_category, created = Category.objects.get_or_create(**new_data)
        recipe = Recipe.objects.create(category=new_category, **validated_data)

        return recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
