from django.contrib import admin
from .models import Product, Category

"""
Register models in Django Admin.
This makes Product and Category visible and manageable in the admin panel.
"""

admin.site.register(Product)  # Register Product model
admin.site.register(Category)  # Register Category model
