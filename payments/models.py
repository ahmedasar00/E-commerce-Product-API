from django.db import models


class Payment(models.Model):
    """
    Represents a payment transaction in the e-commerce application.

    This model stores details about individual payment transactions,
    including the amount, payment method, and status. It also links a
    to the associated order.

    Attributes:
        order (OneToOneField): A link to the associated order.
        amount (DecimalField): The amount of the payment.
        payment_method (CharField): The method used for the payment (e.g., 'Credit Card', 'PayPal').
        transaction_id (CharField): A unique identifier for the payment transaction.
        status (CharField): The current status of the payment (e.g., 'Pending', 'Completed', 'Failed').
        created_at (DateTimeField): Records when the payment was created.
        updated_at (DateTimeField): Records when the payment was last updated.
    """

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
    )

    PAYMENT_METHOD_CHOICES = (
        ("Credit Card", "Credit Card"),
        ("PayPal", "PayPal"),
        ("Stripe", "Stripe"),
    )

    order = models.OneToOneField(
        "orders.Order", on_delete=models.CASCADE, related_name="payment"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default="Credit Card"
    )
    transaction_id = models.CharField(
        max_length=100, unique=True, blank=True, null=True
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the Payment model.

        - db_table: Sets a custom table name in the database.
        - ordering: Sets the default sort order for payments to be by creation date.
        """

        db_table = "Payments"
        ordering = ["-created_at"]

    def __str__(self):
        """
        Returns a human-readable string representation of the payment.
        """
        return f"Payment for Order #{self.order.id} - ${self.amount} - {self.status}"
