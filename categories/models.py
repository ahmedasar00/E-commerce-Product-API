from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    """
    Represents a product category in the e-commerce system.

    This model is used to group products. It includes a name, an
    optional description and image, and automatically generates a
    URL-friendly 'slug' from the name for cleaner web addresses.

    Attributes:
        name (CharField): The required name of the category.
        description (TextField): An optional text description.
        image (ImageField): An optional image for the category.
        created_at (DateTimeField): Records when the category was created.
        updated_at (DateTimeField): Records when the category was last updated.
        slug (SlugField): A URL-friendly version of the name.
    """
    name = models.CharField(max_length=70)
    description = models.TextField(null=True, blank=True, help_text="Description of the Category")
    image = models.ImageField(upload_to='Categories/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        """
        Meta options for the Category model.

        - db_table: Sets a custom table name in the database.
        - ordering: Sets the default sort order for categories to be by name.
        """
        db_table = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to auto-generate the slug.

        If the category is saved without a slug, this method will
        create one from the category's name before committing to the database.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns a human-readable string representation of the category.
        """
        return self.name