from rest_framework import serializers
from .models import Users, Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for the Address mode
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
        # The user field is implicitly read-only because it's set by the view,
        # not sent in the request body when creating an address.


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom Users model.

    Handles creating, updating, and retrieving users with their associated addresses.
    Password hashing is handled securely.
    """

    # Use the AddressSerializer to display a nested list of addresses.
    # This is read-only because addresses should be managed via their own endpoint.
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        # Define the fields to be included in the API representation.
        fields = (
            "id",
            "username",
            "name",
            "email",
            "bio",
            "role",
            "phone",
            "profile_image",
            "addresses",  # The nested addresses will appear here
            "password",  # Include password for creation/update
        )

        # Ensure the password is write-only for security.
        # It can be used to create/update a user but will not be sent in responses.
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create and return a new user with a properly hashed password.
        """
        user = Users.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            # You can add other fields from validated_data here as well
            name=validated_data.get("name", ""),
            role=validated_data.get("role", Users.Roles.CUSTOMER),
        )
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing user instance.

        Handles password updates securely by using set_password if a new
        password is provided.
        """
        # Remove password from the data if it exists and handle it separately.
        password = validated_data.pop("password", None)

        # Update the rest of the fields as usual.
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
