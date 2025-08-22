from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    """
    Represents a product category in the e-commerce system.
    Includes name, optional description, optional image, timestamps, and a slug for URLs.
    """

    name = models.CharField(max_length=70)
    description = models.TextField(null=True, blank=True, help_text="Description of the Category")
    image = models.ImageField(upload_to='Categories/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Override save method to automatically generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
   
    class Meta:
        db_table = 'Categories'
        ordering = ['name']
  
    def __str__(self):
        """
        Return a readable string representation of the category.
        """
        return self.name
