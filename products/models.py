from django.db import models
from categories.models import Category
from django.core.validators import MinValueValidator
from django.utils import timezone

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)]
    )
    stack = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    category = models.ForeignKey(
        "categories.Category", on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField(null=True, blank=True, help_text="Description The Product")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now= True)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products', null=True, blank=True)
    


    class Meta:
        db_table = 'Products'
        ordering = ['name']
        

    def __str__(self):
        return f"{self.name} - ${self.price}"

    
    def save(self, *args, **Kwargs):
        if self.stack <=0:
            self.is_available = False
        else:
            self.is_available = True
        super().save(*args, **Kwargs)
        