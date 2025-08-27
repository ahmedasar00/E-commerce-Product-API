from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users

        fields = ("id", "username", "email", "password", "created_at", "updated_at")
        extra_kwargs = {"password": {"write_only": True}}

        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        """
        Creates and returns a new user with an encrypted password.
        """

        user = Users.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
