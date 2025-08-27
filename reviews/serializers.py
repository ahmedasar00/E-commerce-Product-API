from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer handles creating and displaying reviews. It ensures that
    the user is automatically set to the currently logged-in user and that a
    user cannot review the same product more than once.
    """

    # We make the 'user' field read-only because we will set it automatically
    # in the view based on the currently authenticated user.
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

        # This validator enforces the unique_together constraint from the model
        # at the serializer level, providing a cleaner error message.
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=["user", "product"],
                message="You have already submitted a review for this product.",
            )
        ]
