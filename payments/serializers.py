from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Payment model.

    Handles the conversion of Payment model instances to JSON format for API
    responses and validates incoming data for creating or updating payments.
    """

    # To make the API response more readable, we can display the order's
    # string representation instead of just its ID.
    order = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Payment

        # Include all fields from the Payment model in the API representation.
        fields = "__all__"

        # These fields are typically set by the system or a payment gateway,
        # not directly by a user through the API.
        read_only_fields = ("created_at", "updated_at")
