from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserRoleEditSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    role_id = serializers.IntegerField()
