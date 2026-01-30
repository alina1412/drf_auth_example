from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField(allow_blank=True)


class UserRoleEditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role_id = serializers.IntegerField()
