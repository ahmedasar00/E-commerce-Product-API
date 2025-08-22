from django.db import models
from categories.models import Category
from django.core.validators import MinValueValidator
from django.utils import timezone

class Product(models.Model):
    """
    Represents a product in the e-commerce application.

    This model stores all the essential details about a product,
    including its name, price, stock level, and category. It also
    contains logic to automatically manage its availability status.

    Attributes:
        name (CharField): The name of the product.
        price (DecimalField): The price of the product.
        stack (IntegerField): The number of items available in stock.
        category (ForeignKey): A link to the product's category.
        description (TextField): An optional, detailed description.
        created_at (DateTimeField): Records when the product was created.
        updated_at (DateTimeField): Records when the product was last updated.
        is_available (BooleanField): True if the product is in stock.
        image (ImageField): An optional image for the product.
    """
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    stack = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField(
        null=True, blank=True, help_text="Enter a brief description of the product"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='products', null=True, blank=True, help_text="Upload an image for the product"
    )

    class Meta:
        """
        Meta options for the Product model.

        - db_table: Sets a custom table name in the database.
        - ordering: Sets the default sort order for products to be by name.
        """
        db_table = 'Products'
        ordering = ['name']

    def __str__(self):
        """
        Returns a human-readable string representation of the product.
        """
        return f"{self.name} - ${self.price}"

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to manage availability.

        This method automatically sets the 'is_available' field to False
        if the stock count is zero or less, ensuring the product cannot
        be purchased.
        """
        if self.stack <= 0:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **kwargs)