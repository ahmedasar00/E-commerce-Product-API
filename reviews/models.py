from django.db import models
from users.models import Users
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    """
    Represents a user's review for a product.

    This model stores the rating and an optional comment that a user
    leaves for a specific product. It includes rules to ensure that the
    rating is between 1 and 5, and that a user can only review a
    product one time.

    Attributes:
        user (ForeignKey): A required link to the user who wrote the review.
        product (ForeignKey): A required link to the product being reviewed.
        rating (IntegerField): A required star rating, must be between 1 and 5.
        comment (TextField): An optional text comment from the user.
        created_at (DateTimeField): Automatically records when the review was created.
        updated_at (DateTimeField): Automatically records when the review was last updated.
    """
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta options for the Review model.
        
        - unique_together: Ensures a user can't review the same product twice.
        - ordering: Sets the default order to show newest reviews first.
        """
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        """
        Returns a human-readable string representation of the review.

        This is used in the Django admin site and other places where the
        object needs to be displayed as text.
        """
        return f"Review by {self.user.username} for {self.product.name}"