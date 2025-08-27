from rest_framework import serializers
from .models import Product
from categories.models import Category


class CategoryLiteSerializer(serializers.ModelSerializer):
    """A simple serializer to represent categories within product details."""

    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This handles the conversion of Product instances to JSON, including
    nested details for the category.
    """

    # Use a nested serializer for the category to show its details,
    # not just its ID. This is read-only.
    category = CategoryLiteSerializer(read_only=True)

    # We need a separate, writeable field to accept the category ID
    # when creating or updating a product.
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "stack",  # Note: 'stock' is the more common spelling
            "category",
            "category_id",
            "description",
            "is_available",
            "image",
            "created_at",
            "updated_at",
        )

        # These fields are set automatically by the model's logic
        # or the database, so they should not be editable via the API.
        read_only_fields = ("is_available", "created_at", "updated_at")
