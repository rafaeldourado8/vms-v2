"""API serializers."""
from rest_framework import serializers


class CreateUserSerializer(serializers.Serializer):
    """Serializer for creating user."""

    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    name = serializers.CharField(max_length=255)


class UserResponseSerializer(serializers.Serializer):
    """Serializer for user response."""

    id = serializers.UUIDField()
    email = serializers.EmailField()
    name = serializers.CharField()
    is_active = serializers.BooleanField()
    roles = serializers.ListField(child=serializers.CharField())


class AssignRoleSerializer(serializers.Serializer):
    """Serializer for assigning role."""

    role_code = serializers.CharField()
