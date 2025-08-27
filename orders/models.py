from django.db import models
from django.conf import settings
from users.models import Address


class Order(models.Model):
    """
    Represents a customer's order in the e-commerce application.

    This model stores the main details of an order, such as the user who
    placed it, its status, and the total amount.

    Attributes:
        user (ForeignKey): The user who placed the order.
        created_at (DateTimeField): The date and time when the order was created.
        status (CharField): The current status of the order (e.g., 'Pending', 'Completed').
        total_amount (DecimalField): The total cost of the order.
    """

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        """
        Meta options for the Order model.

        - db_table: Sets a custom table name in the database.
        - ordering: Sets the default sort order for orders to be by creation date.
        """

        db_table = "Orders"
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a human-readable string representation of the order.
        """
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    """
    Represents an item within an order.

    This model links a product to an order, specifying the quantity and the
    price at the time the order was placed.

    Attributes:
        order (ForeignKey): The order this item belongs to.
        product (ForeignKey): The product being ordered.
        quantity (PositiveIntegerField): The quantity of the product ordered.
        price_at_order_time (DecimalField): The price of the product when the order was made.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        """
        Meta options for the OrderItem model.

        - db_table: Sets a custom table name in the database.
        """

        db_table = "OrderItems"

    def __str__(self):
        """
        Returns a human-readable string representation of the order item.
        """
        return f"{self.quantity} x {self.product.name}"
