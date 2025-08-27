from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from users.models import Address


class ProductLiteSerializer(serializers.ModelSerializer):
    """
    A simple serializer for the Product model.
    It only includes the id, name, and price of the product.
    """

    class Meta:
        model = Product
        fields = ("id", "name", "price")


class OrderItemSerializer(serializers.ModelSerializer):
    """
    A serializer for the OrderItem model.
    It shows the product details, quantity, and the price when the order was made.
    """

    product = ProductLiteSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "quantity", "price_at_order_time")


class OrderSerializer(serializers.ModelSerializer):
    """
    A serializer for the Order model.
    It shows all the details of an order, including the user, address,
    status, total amount, and all the items in the order.
    """

    user = serializers.StringRelatedField(read_only=True)
    address = serializers.StringRelatedField(read_only=True)

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "address",
            "status",
            "total_amount",
            "created_at",
            "items",
        )
