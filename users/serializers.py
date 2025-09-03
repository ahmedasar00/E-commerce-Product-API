from rest_framework import serializers
from .models import Users, Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address model.
    Converts Address objects into JSON and vice versa.
    """

    class Meta:
        model = Address
        fields = (
            "id",
            "street",
            "city",
            "state",
            "country",
            "postal_code",
            "is_default",
        )
        # The "user" field is not exposed here.
        # It will be set by the view, not directly by the client.


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom Users model.

    - Supports creating, updating, and retrieving users.
    - Handles password hashing securely.
    - Includes nested addresses (read-only).
    """

    # Nested serializer for related addresses (read-only)
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = (
            "id",
            "username",
            "name",
            "email",
            "bio",
            "role",
            "phone",
            "profile_image",
            "addresses",  # Nested addresses appear here
            "password",  # For create/update only (write-only)
        )

        # Password can be written but never returned in API responses
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a new user with a hashed password.
        """
        user = Users.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data.get("name", ""),
            role=validated_data.get("role", Users.Roles.CUSTOMER),
        )
        return user

    def update(self, instance, validated_data):
        """
        Update an existing user.
        If a new password is provided, hash it before saving.
        """
        password = validated_data.pop("password", None)  # Handle password separately
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
